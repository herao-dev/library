#!/usr/bin/env python3
"""
课程设计说明书生成器
为"图书管理系统" Flask Web 应用生成 .docx 格式的课程设计报告。
参照: 课程设计说明书样本.doc 的格式
"""
import os
import sys
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ============================================================
# Configuration
# ============================================================
FONT_BODY = '宋体'
FONT_HEADING = '黑体'
FONT_ENGLISH = 'Times New Roman'
FONT_CODE = 'Consolas'

OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILENAME = '图书管理系统_课程设计说明书.docx'


# ============================================================
# Low-level Helper Functions
# ============================================================
def set_run_font(run, font_cn, font_en=FONT_ENGLISH, size=Pt(12), bold=False, color=None):
    """Set both CJK and Latin fonts on a run."""
    run.font.size = size
    run.font.name = font_en
    run.font.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_cn)
    if color:
        run.font.color.rgb = color


def add_formatted_paragraph(doc, text, font_name=FONT_BODY, size=Pt(12),
                            bold=False, alignment=None, space_after=Pt(6),
                            space_before=Pt(0), first_line_indent=None,
                            line_spacing=1.5):
    """Add a paragraph with proper Chinese font support."""
    p = doc.add_paragraph()
    if alignment is not None:
        p.alignment = alignment
    pf = p.paragraph_format
    pf.space_after = space_after
    pf.space_before = space_before
    pf.line_spacing = line_spacing
    if first_line_indent:
        pf.first_line_indent = first_line_indent
    run = p.add_run(text)
    set_run_font(run, font_name, size=size, bold=bold)
    return p


def add_heading_text(doc, number, title, level=1):
    """Add a numbered section heading with proper font."""
    sizes = {1: Pt(16), 2: Pt(14), 3: Pt(13)}
    size = sizes.get(level, Pt(12))
    text = f'{number} {title}'
    space_before_map = {1: Pt(18), 2: Pt(12), 3: Pt(8)}
    if level == 1:
        doc.add_page_break()
    p = add_formatted_paragraph(doc, text, font_name=FONT_HEADING, size=size,
                                bold=True, space_after=Pt(10),
                                space_before=space_before_map.get(level, Pt(6)))
    return p


def add_body(doc, text):
    """Add body paragraph with first-line indent of two Chinese characters."""
    return add_formatted_paragraph(doc, text, font_name=FONT_BODY, size=Pt(12),
                                   first_line_indent=Cm(0.74))


def add_blank_line(doc):
    """Add an empty line."""
    add_formatted_paragraph(doc, '', space_after=Pt(0), line_spacing=1.0)


def set_cell_text(cell, text, font_name=FONT_BODY, size=Pt(9), bold=False,
                  alignment=WD_ALIGN_PARAGRAPH.LEFT):
    """Set text in a table cell with proper font."""
    cell.text = ''
    p = cell.paragraphs[0]
    p.alignment = alignment
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    run = p.add_run(str(text))
    set_run_font(run, font_name, size=size, bold=bold)


def shade_cell(cell, color='D9E2F3'):
    """Add background shading to a cell."""
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    shading.set(qn('w:val'), 'clear')
    cell._element.tcPr.append(shading)


def add_table(doc, headers, rows, col_widths=None, header_font=FONT_HEADING):
    """Add a formatted table."""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Header row
    for i, header in enumerate(headers):
        cell = table.cell(0, i)
        set_cell_text(cell, header, font_name=header_font, size=Pt(9),
                      bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER)
        shade_cell(cell)
    # Data rows
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.cell(r + 1, c)
            set_cell_text(cell, val, size=Pt(9))
    if col_widths:
        for i, width in enumerate(col_widths):
            for row_obj in table.rows:
                row_obj.cells[i].width = width
    add_blank_line(doc)
    return table


def add_image_placeholder(doc, caption_text, fig_label=''):
    """Add a bordered placeholder box for a missing screenshot."""
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    # Force cell height with paragraphs
    cell.paragraphs[0].clear()
    for _ in range(4):
        inner_p = cell.add_paragraph()
        inner_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        inner_p.paragraph_format.space_after = Pt(12)
        inner_p.paragraph_format.space_before = Pt(12)
    cell.paragraphs[0].clear()
    p_top = cell.paragraphs[0]
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.space_before = Pt(36)
    run = p_top.add_run(caption_text)
    set_run_font(run, FONT_BODY, size=Pt(11), color=RGBColor(150, 150, 150))
    p_bottom = cell.paragraphs[1]
    p_bottom.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_bottom.paragraph_format.space_after = Pt(36)
    run2 = p_bottom.add_run('（请替换为实际截图）')
    set_run_font(run2, FONT_BODY, size=Pt(9), color=RGBColor(180, 180, 180))
    # Figure caption
    if fig_label:
        cap_p = add_formatted_paragraph(doc, fig_label, font_name=FONT_BODY,
                                        size=Pt(10), alignment=WD_ALIGN_PARAGRAPH.CENTER,
                                        space_after=Pt(12))
    return table


def add_code_block(doc, code_text, label=''):
    """Add a code block with monospace font and gray background."""
    if label:
        add_formatted_paragraph(doc, label, font_name=FONT_HEADING, size=Pt(10),
                                bold=True, space_after=Pt(4))
    table = doc.add_table(rows=1, cols=1)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), 'F2F2F2')
    shading.set(qn('w:val'), 'clear')
    cell._element.tcPr.append(shading)
    cell.paragraphs[0].paragraph_format.space_after = Pt(0)
    cell.paragraphs[0].paragraph_format.space_before = Pt(0)
    for i, line in enumerate(code_text.strip().split('\n')):
        if i == 0:
            p = cell.paragraphs[0]
        else:
            p = cell.add_paragraph()
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.line_spacing = 1.1
        run = p.add_run(line)
        set_run_font(run, FONT_CODE, font_en=FONT_CODE, size=Pt(8))
    add_blank_line(doc)


# ============================================================
# Page Setup
# ============================================================
def setup_page(doc):
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(3.17)


def setup_header_footer(doc):
    section = doc.sections[0]
    # Header
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = hp.add_run('《web应用与开发课程设计》')
    set_run_font(run, FONT_BODY, size=Pt(9))
    # Footer with page number
    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run1 = fp.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    run1._r.append(fldChar1)
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' PAGE '
    run1._r.append(instrText)
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    run1._r.append(fldChar2)
    run2 = fp.add_run('1')
    set_run_font(run2, FONT_ENGLISH, size=Pt(9))
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run2._r.append(fldChar3)


# ============================================================
# Cover Page
# ============================================================
def build_cover(doc):
    # University emblem placeholder
    for _ in range(4):
        add_blank_line(doc)
    add_image_placeholder(doc, '[校徽]', '')
    add_image_placeholder(doc, '[大学名称图片]', '')

    for _ in range(3):
        add_blank_line(doc)

    # Course title
    add_formatted_paragraph(doc, '《web应用与开发》课程设计说明书',
                            font_name=FONT_HEADING, size=Pt(22),
                            bold=True, alignment=WD_ALIGN_PARAGRAPH.CENTER,
                            space_after=Pt(36))

    # Info fields
    info_items = [
        ('题    目：', '图书管理系统的设计与实现'),
        ('系    别：', '计算机科学与技术系'),
        ('专业班级：', '专升本   班'),
        ('学    号：', '________________________'),
        ('姓    名：', '________________________'),
        ('指导教师：', '刘兴明'),
    ]

    for label, value in info_items:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_after = Pt(10)
        p.paragraph_format.line_spacing = 2.0
        run_label = p.add_run(label)
        set_run_font(run_label, FONT_BODY, size=Pt(14))
        run_value = p.add_run(value)
        set_run_font(run_value, FONT_BODY, size=Pt(14))

    add_blank_line(doc)
    add_formatted_paragraph(doc, '2026年  5月  10日', font_name=FONT_BODY,
                            size=Pt(14), alignment=WD_ALIGN_PARAGRAPH.CENTER,
                            space_after=Pt(6))
    doc.add_page_break()


# ============================================================
# Table of Contents
# ============================================================
def build_toc(doc):
    add_heading_text(doc, '', '目    录', level=1)
    add_blank_line(doc)

    # TOC field code
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run()
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')
    run._r.append(fldChar_begin)

    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' TOC \\o "1-3" \\h \\z '
    run._r.append(instrText)

    fldChar_separate = OxmlElement('w:fldChar')
    fldChar_separate.set(qn('w:fldCharType'), 'separate')
    run._r.append(fldChar_separate)

    note_run = p.add_run('（打开文档后，请右键点击此处 → "更新域" → "更新整个目录"以生成目录）')
    set_run_font(note_run, FONT_BODY, size=Pt(10), color=RGBColor(128, 128, 128))

    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')
    note_run._r.append(fldChar_end)


# ============================================================
# Section 1: 设计任务与要求
# ============================================================
def build_section1(doc):
    add_heading_text(doc, '1', '设计任务与要求')

    add_heading_text(doc, '1.1', '总体目标与任务要求', level=2)
    add_body(doc, '本次课程设计的总体目标是设计并实现一个基于Web的图书管理系统。该系统以Python Flask框架为核心，采用B/S（浏览器/服务器）架构，为图书馆或图书室提供一套完整的信息化管理解决方案。系统需要支持图书的增删改查、借阅与归还管理、读者预约排队、评论评分、公告发布以及用户管理等功能，能够满足管理员和普通读者两类用户的使用需求。')
    add_body(doc, '任务要求方面，系统需要完成以下核心开发工作：一是搭建Flask Web应用基础框架，采用应用工厂模式和蓝图（Blueprint）架构实现模块化设计；二是设计合理的数据库模型，使用MySQL关系型数据库配合SQLAlchemy ORM进行数据持久化；三是实现完整的用户认证与权限控制体系，区分管理员与普通用户两种角色；四是开发管理后台与用户前台两套界面，分别满足不同角色的操作需求；五是实现借阅归还核心业务流程，包括自动计算逾期罚金、库存实时更新等功能。')

    add_heading_text(doc, '1.2', '题目选择与目的意义', level=2)
    add_body(doc, '选择"图书管理系统"作为课程设计题目的原因主要有三个方面。首先，图书管理是一个具有普遍现实需求的应用场景，无论是学校图书馆、社区图书室还是企业内部资料室，都需要一套高效的信息化管理系统来替代传统的手工记录方式。Web化部署使得系统可以跨平台访问，无需安装客户端软件，极大降低了使用门槛。')
    add_body(doc, '其次，从技术学习角度来看，图书管理系统涵盖了Web开发全流程的各个关键技术点：数据库设计与ORM映射、表单验证与CSRF防护、用户认证与会话管理、模板渲染与前端交互、RESTful API设计等。这些技术的综合运用能够充分体现《web应用与开发》课程所教授的核心知识和技能。')
    add_body(doc, '最后，该题目具有良好的可扩展性。在完成基础功能后，可以继续深入开发邮件通知、数据导出、扫码录入、容器化部署等进阶功能，为后续学习提供持续改进的空间。通过这个项目的实践，能够建立起完整的全栈Web开发能力，对未来的毕业设计和实际工作都具有积极的参考价值。')

    add_heading_text(doc, '1.3', '所选题目的主要工作', level=2)
    add_body(doc, '本系统的主要工作涵盖后端开发、前端开发、数据库设计和系统集成四个方面。后端开发基于Flask框架，采用蓝图（Blueprint）模式将会员认证（auth）、管理后台（admin）、用户前台（user）和API接口（api）四个功能模块进行解耦。共设计7个数据模型（User、Category、Book、BorrowRecord、Reservation、Review、Announcement），实现了约50条路由，涵盖用户注册登录、图书CRUD、分类管理、借阅归还与逾期罚金自动计算、预约排队、评论评分和公告发布等完整业务功能。')
    add_body(doc, '前端开发采用Jinja2模板引擎进行服务端渲染，使用Bootstrap 5框架构建响应式用户界面，配合Bootstrap Icons图标库和Google Fonts（Inter字体）提升视觉体验。编写了约1100行自定义CSS样式代码，定义了完整的设计系统（颜色变量、阴影、圆角、间距规范等）。管理后台提供了17个功能页面，用户前台提供了7个功能页面，统一通过布局模板（base.html、admin.html、user.html）和可复用组件（导航栏、侧边栏、分页器、确认弹窗等）构建。')
    add_body(doc, '数据库设计方面，根据业务需求设计了7张数据表，建立了合理的外键关联和索引。编写了完整的建库SQL脚本（library.sql）和增量迁移脚本（migrate.sql），包含约20条种子数据用于系统初始化。此外，还编写了豆瓣图书封面自动获取脚本（fetch_book_covers.py），能够通过公开API批量下载图书封面图片。')


# ============================================================
# Section 2: 需求分析
# ============================================================
def build_section2(doc):
    add_heading_text(doc, '2', '需求分析')

    add_heading_text(doc, '2.1', '功能需求分析', level=2)
    add_body(doc, '本系统面向两类用户角色：管理员（Admin）和普通用户（User），每种角色具有不同的功能需求。以下从用户认证、图书管理、借阅管理、预约管理、评论管理和公告管理六个维度进行详细分析。')

    add_heading_text(doc, '2.1.1', '用户认证模块', level=3)
    add_body(doc, '系统需要提供完整的用户注册与登录功能。注册时需验证用户名和邮箱的唯一性，密码通过Werkzeug的scrypt算法进行哈希存储，确保安全性。登录后基于Flask-Login维护会话状态，系统根路由根据用户角色自动重定向到对应的管理后台或用户首页。未登录用户访问任何受保护页面时自动跳转到登录页。')

    add_heading_text(doc, '2.1.2', '图书管理模块', level=3)
    add_body(doc, '管理员需要对图书进行全生命周期管理，包括：添加新书（书名、作者、ISBN、出版社、出版日期、分类、总库存、可借库存、描述、馆藏位置、封面图片上传）；编辑已有图书信息；删除图书（需检查是否存在未归还的借阅记录）；按书名、作者、ISBN进行模糊搜索；按分类筛选；分页浏览。普通用户则需要在图书浏览页面查看图书列表（以卡片形式展示，包含封面图、书名、作者、借阅状态），支持搜索和分类筛选，并能进入图书详情页查看完整信息、读者评论和评分。')

    add_heading_text(doc, '2.1.3', '借阅管理模块', level=3)
    add_body(doc, '这是系统的核心业务模块。借书时需检查库存（available_copies > 0）和用户的重复借阅状态，创建借阅记录时将借阅日期设为当前时间，应还日期为30天后（BORROW_DAYS配置项），同时将图书可借库存减1。还书时记录实际归还日期，自动计算逾期天数并按每天0.50元的标准计算罚金，将可借库存加1。系统需在每次查询借阅记录时自动检测逾期状态：对于已过应还日期但仍处于"已借出"状态的记录，自动将其标记为"逾期"。借阅状态分为三种：已借出（borrowed）、已归还（returned）、逾期（overdue）。')

    add_heading_text(doc, '2.1.4', '预约管理模块', level=3)
    add_body(doc, '当图书库存为0时，用户可选择预约该图书。预约记录创建后状态为"待处理"（pending），当图书被归还时系统会自动查找最早的待处理预约。预约状态包括：待处理（pending）、已满足（fulfilled）、已取消（cancelled）、已过期（expired）。用户和管理员均可取消预约。每个用户对同一本图书只能有一条待处理状态的预约记录。')

    add_heading_text(doc, '2.1.5', '评论评分模块', level=3)
    add_body(doc, '用户需满足"曾经借阅过该图书"的条件才能发表评论。评论包含1-5星评分和文字内容，每位用户对每本图书只能有一条评论（再次提交则更新）。评论发表后默认可见，管理员可在后台审核：切换显示/隐藏状态，或删除不当评论。图书详情页展示所有可见评论，并计算平均评分。')

    add_heading_text(doc, '2.1.6', '公告管理模块', level=3)
    add_body(doc, '管理员可发布、编辑、上下架和删除公告。公告属性包括标题、正文内容、优先级（普通/重要/紧急）和发布状态。已发布的公告按创建时间倒序展示在管理后台首页和用户首页。公告发布者关联到当前登录的管理员账号。')

    add_heading_text(doc, '2.2', '功能模块设计', level=2)
    add_body(doc, '根据功能需求分析，系统采用Flask蓝图（Blueprint）进行模块划分，共分为四个蓝图模块，各模块之间通过数据库模型层共享数据，通过装饰器实现权限控制。')

    add_table(doc,
        ['蓝图模块', 'URL前缀', '权限要求', '功能概述'],
        [
            ['auth (认证模块)', '/auth', '公开访问',
             '用户注册、登录、登出。包含注册表单验证（用户名/邮箱唯一性检查），登录凭据验证，登出会话清除。'],
            ['admin (管理后台)', '/admin', '需登录 + 管理员角色',
             '管理控制台统计概览、图书CRUD、分类管理、用户管理（含启用/禁用）、借阅管理（含借书/还书/罚金计算）、预约管理、评论审核、公告管理。共计约30条路由。'],
            ['user (用户前台)', '/user', '需登录',
             '用户个人首页、图书浏览与详情（含借阅/预约/评论操作）、个人借阅记录、个人预约记录、个人信息编辑、密码修改。共计约15条路由。'],
            ['api (数据接口)', '/api', '需登录',
             '图书搜索建议（AJAX JSON接口）、用户搜索建议（需管理员权限）、借阅统计数据（需管理员权限）。共计3条路由。'],
        ],
        col_widths=[Cm(2.5), Cm(1.5), Cm(2.8), Cm(7.5)]
    )

    add_body(doc, '系统的模块层次结构如图2-1功能模块图所示。四个蓝图模块围绕7个数据模型进行协作：认证模块负责用户身份验证，管理模块与用户模块共享图书、借阅、预约、评论、公告等数据，API模块为前端AJAX交互提供轻量级JSON数据接口。所有模块均使用Flask-SQLAlchemy进行数据库操作，通过Flask-WTF实现CSRF跨站请求伪造防护。')

    add_image_placeholder(doc, '[功能模块结构图]', '图2-1 系统功能模块图')


# ============================================================
# Section 3: 系统设计
# ============================================================
def build_section3(doc):
    add_heading_text(doc, '3', '系统设计')

    # --- 3.1 Database Design ---
    add_heading_text(doc, '3.1', '数据库设计', level=2)
    add_body(doc, '系统采用MySQL关系型数据库，使用Flask-SQLAlchemy作为ORM框架进行数据库操作。根据业务需求分析，共设计7张数据表，涵盖用户、图书分类、图书、借阅记录、预约记录、评论和公告。各表之间通过外键建立关联关系，确保数据的一致性和完整性。开发阶段也可使用SQLite内存数据库进行快速测试。')

    add_heading_text(doc, '3.1.1', '系统E-R图', level=3)
    add_body(doc, '系统的实体-关系（E-R）模型包含以下核心实体及其关系：用户（User）与借阅记录（BorrowRecord）之间为一对多关系，一个用户可以有多条借阅记录；用户与预约记录（Reservation）之间为一对多关系；用户与评论（Review）之间为一对多关系；图书分类（Category）与图书（Book）之间为一对多关系，一个分类下可包含多本图书；图书与借阅记录之间为一对多关系；图书与预约记录之间为一对多关系；图书与评论之间为一对多关系；用户（作为发布者）与公告（Announcement）之间为一对多关系。')

    add_image_placeholder(doc, '[系统E-R图]', '图3-1 系统E-R图')

    # 3.1.2 User table
    add_heading_text(doc, '3.1.2', '用户表（user）', level=3)
    add_body(doc, '用户表存储系统用户的基本信息，包括登录凭据、角色权限和个人资料。密码使用Werkzeug提供的scrypt算法进行哈希存储，不可逆。role字段区分管理员（admin）和普通用户（user）两种角色，is_active字段支持账号的启用/禁用管理。')

    add_table(doc,
        ['字段名', '数据类型', '约束', '说明'],
        [
            ['id', 'INT', '主键，自增', '用户唯一标识'],
            ['username', 'VARCHAR(64)', 'UNIQUE, NOT NULL', '用户名'],
            ['email', 'VARCHAR(128)', 'UNIQUE, NOT NULL', '电子邮箱'],
            ['password_hash', 'VARCHAR(256)', 'NOT NULL', '密码哈希值（scrypt算法）'],
            ['role', 'VARCHAR(16)', 'NOT NULL, DEFAULT \'user\'', '角色：admin或user'],
            ['phone', 'VARCHAR(20)', 'NULL', '手机号码'],
            ['avatar', 'VARCHAR(256)', 'NULL', '头像图片路径'],
            ['is_active', 'BOOLEAN', 'NOT NULL, DEFAULT TRUE', '账号启用状态'],
            ['created_at', 'DATETIME', 'NOT NULL, DEFAULT NOW', '创建时间'],
            ['updated_at', 'DATETIME', 'NOT NULL, ON UPDATE NOW', '更新时间'],
        ],
        col_widths=[Cm(2.4), Cm(2.6), Cm(3.0), Cm(4.0)]
    )

    # 3.1.3 Category table
    add_heading_text(doc, '3.1.3', '分类表（category）', level=3)
    add_body(doc, '分类表存储图书分类信息，与图书表形成一对多关系。分类名称具有唯一性约束。删除分类前需检查该分类下是否还有关联图书。')

    add_table(doc,
        ['字段名', '数据类型', '约束', '说明'],
        [
            ['id', 'INT', '主键，自增', '分类唯一标识'],
            ['name', 'VARCHAR(64)', 'UNIQUE, NOT NULL', '分类名称'],
            ['description', 'TEXT', 'NULL', '分类描述'],
            ['created_at', 'DATETIME', 'NOT NULL, DEFAULT NOW', '创建时间'],
        ],
        col_widths=[Cm(2.4), Cm(2.6), Cm(3.0), Cm(4.0)]
    )

    # 3.1.4 Book table
    add_heading_text(doc, '3.1.4', '图书表（book）', level=3)
    add_body(doc, '图书表是系统的核心数据表，存储图书的详细信息。isbn字段具有唯一性约束（但允许为空）。total_copies记录图书的总副本数，available_copies记录当前可借副本数，二者的差值即为当前被借出的副本数。category_id通过外键关联到分类表，删除分类时该字段设为NULL。')

    add_table(doc,
        ['字段名', '数据类型', '约束', '说明'],
        [
            ['id', 'INT', '主键，自增', '图书唯一标识'],
            ['title', 'VARCHAR(256)', 'NOT NULL', '书名'],
            ['author', 'VARCHAR(128)', 'NOT NULL', '作者'],
            ['isbn', 'VARCHAR(20)', 'UNIQUE, NULL', 'ISBN编号'],
            ['publisher', 'VARCHAR(128)', 'NULL', '出版社'],
            ['publish_date', 'DATE', 'NULL', '出版日期'],
            ['category_id', 'INT', 'FK→category.id, ON DELETE SET NULL', '所属分类'],
            ['total_copies', 'INT', 'NOT NULL, DEFAULT 1', '总副本数'],
            ['available_copies', 'INT', 'NOT NULL, DEFAULT 1', '可借副本数'],
            ['cover_image', 'VARCHAR(256)', 'NULL', '封面图片路径'],
            ['description', 'TEXT', 'NULL', '图书简介'],
            ['location', 'VARCHAR(64)', 'NULL', '馆藏位置'],
            ['created_at', 'DATETIME', 'NOT NULL, DEFAULT NOW', '创建时间'],
            ['updated_at', 'DATETIME', 'NOT NULL, ON UPDATE NOW', '更新时间'],
        ],
        col_widths=[Cm(2.2), Cm(2.2), Cm(3.0), Cm(4.6)]
    )

    # 3.1.5 BorrowRecord table
    add_heading_text(doc, '3.1.5', '借阅记录表（borrow_record）', level=3)
    add_body(doc, '借阅记录表存储每一次借阅操作的完整信息。借阅时记录借阅日期（borrow_date）和应还日期（due_date），归还时记录实际归还日期（return_date）并自动计算逾期罚金。状态字段支持三种取值：borrowed（已借出）、returned（已归还）、overdue（逾期）。罚金计算标准为逾期天数 × 0.50元/天。user_id和book_id分别通过外键关联到用户表和图书表，删除用户或图书时级联删除相关借阅记录。')

    add_table(doc,
        ['字段名', '数据类型', '约束', '说明'],
        [
            ['id', 'INT', '主键，自增', '借阅记录唯一标识'],
            ['user_id', 'INT', 'FK→user.id, ON DELETE CASCADE', '借阅用户'],
            ['book_id', 'INT', 'FK→book.id, ON DELETE CASCADE', '所借图书'],
            ['borrow_date', 'DATETIME', 'NOT NULL, DEFAULT NOW', '借阅日期'],
            ['due_date', 'DATETIME', 'NOT NULL', '应还日期（借阅日期+30天）'],
            ['return_date', 'DATETIME', 'NULL', '实际归还日期'],
            ['status', 'VARCHAR(16)', 'NOT NULL, DEFAULT \'borrowed\'', '状态：borrowed/returned/overdue'],
            ['fine', 'NUMERIC(10,2)', 'NOT NULL, DEFAULT 0.00', '逾期罚金（元）'],
            ['created_at', 'DATETIME', 'NOT NULL, DEFAULT NOW', '创建时间'],
            ['updated_at', 'DATETIME', 'NOT NULL, ON UPDATE NOW', '更新时间'],
        ],
        col_widths=[Cm(2.2), Cm(2.4), Cm(3.0), Cm(4.4)]
    )

    # 3.1.6 Reservation table
    add_heading_text(doc, '3.1.6', '预约表（reservation）', level=3)
    add_body(doc, '预约表记录用户对图书的预约信息。当图书库存为0时，用户可提交预约。预约状态包括：pending（待处理）、fulfilled（已满足）、cancelled（已取消）、expired（已过期）。reserve_date记录预约提交时间，notify_date记录通知用户的时间，expire_date记录预约到期时间。')

    add_table(doc,
        ['字段名', '数据类型', '约束', '说明'],
        [
            ['id', 'INT', '主键，自增', '预约记录唯一标识'],
            ['user_id', 'INT', 'FK→user.id, CASCADE', '预约用户'],
            ['book_id', 'INT', 'FK→book.id, CASCADE', '预约图书'],
            ['reserve_date', 'DATETIME', 'NOT NULL, DEFAULT NOW', '预约日期'],
            ['status', 'VARCHAR(16)', 'NOT NULL, DEFAULT \'pending\'', '状态：pending/fulfilled/cancelled/expired'],
            ['notify_date', 'DATETIME', 'NULL', '通知日期'],
            ['expire_date', 'DATETIME', 'NULL', '过期日期'],
            ['created_at', 'DATETIME', 'NOT NULL, DEFAULT NOW', '创建时间'],
        ],
        col_widths=[Cm(2.2), Cm(2.4), Cm(3.0), Cm(4.4)]
    )

    # 3.1.7 Review table
    add_heading_text(doc, '3.1.7', '评论表（review）', level=3)
    add_body(doc, '评论表记录用户对图书的评分和评论内容。用户需借阅过该图书才能发表评论。每位用户对每本图书只能有一条评论记录（再次提交则更新评分和内容）。is_visible字段支持管理员对评论进行显示/隐藏控制。rating字段存储1-5的整数评分。')

    add_table(doc,
        ['字段名', '数据类型', '约束', '说明'],
        [
            ['id', 'INT', '主键，自增', '评论唯一标识'],
            ['user_id', 'INT', 'FK→user.id, CASCADE', '评论用户'],
            ['book_id', 'INT', 'FK→book.id, CASCADE', '被评图书'],
            ['rating', 'INT', 'NOT NULL, DEFAULT 5', '评分（1-5）'],
            ['content', 'TEXT', 'NULL', '评论内容'],
            ['is_visible', 'BOOLEAN', 'NOT NULL, DEFAULT TRUE', '是否可见'],
            ['created_at', 'DATETIME', 'NOT NULL, DEFAULT NOW', '创建时间'],
        ],
        col_widths=[Cm(2.2), Cm(2.4), Cm(3.0), Cm(4.4)]
    )

    # 3.1.8 Announcement table
    add_heading_text(doc, '3.1.8', '公告表（announcement）', level=3)
    add_body(doc, '公告表存储管理员发布的公告信息。priority字段支持三种优先级：normal（普通）、important（重要）、urgent（紧急）。is_published字段控制公告的发布/下架状态。publisher_id关联到发布该公告的管理员用户。')

    add_table(doc,
        ['字段名', '数据类型', '约束', '说明'],
        [
            ['id', 'INT', '主键，自增', '公告唯一标识'],
            ['title', 'VARCHAR(256)', 'NOT NULL', '公告标题'],
            ['content', 'TEXT', 'NOT NULL', '公告内容'],
            ['priority', 'VARCHAR(16)', 'NOT NULL, DEFAULT \'normal\'', '优先级：normal/important/urgent'],
            ['is_published', 'BOOLEAN', 'NOT NULL, DEFAULT TRUE', '是否发布'],
            ['publisher_id', 'INT', 'FK→user.id, ON DELETE SET NULL', '发布者'],
            ['created_at', 'DATETIME', 'NOT NULL, DEFAULT NOW', '创建时间'],
            ['updated_at', 'DATETIME', 'NOT NULL, ON UPDATE NOW', '更新时间'],
        ],
        col_widths=[Cm(2.2), Cm(2.4), Cm(3.0), Cm(4.4)]
    )

    # --- 3.2-3.12 UI Design ---
    add_heading_text(doc, '3.2', '系统架构设计', level=2)
    add_body(doc, '系统采用经典的MVC（Model-View-Controller）分层架构模式。Model层由7个SQLAlchemy数据模型组成，负责数据持久化和业务逻辑；View层使用Jinja2模板引擎进行服务端渲染，配合Bootstrap 5框架实现响应式UI；Controller层由Flask蓝图中的路由函数承担，接收HTTP请求、调用Model层处理业务、向View层传递数据。应用工厂模式（create_app函数）根据环境变量加载不同配置（开发/生产/测试），实现了配置与代码的分离。系统架构如图3-2所示。')

    add_image_placeholder(doc, '[系统架构图]', '图3-2 系统架构图')

    add_heading_text(doc, '3.3', '应用工厂与蓝图注册', level=2)
    add_body(doc, '应用入口通过create_app()工厂函数创建Flask实例。该函数依次完成：加载配置类（Config）、初始化扩展（数据库ORM、迁移工具、登录管理器、CSRF保护）、注册四个蓝图模块（auth、admin、user、api）并设置URL前缀、注册CLI命令（flask seed种子数据命令）、创建文件上传目录。根路由（/）根据用户认证状态和角色进行智能重定向：已登录管理员跳转至admin.dashboard，已登录用户跳转至user.dashboard，未登录用户跳转至auth.login。')

    add_heading_text(doc, '3.4', '登录界面设计', level=2)
    add_body(doc, '登录界面（/auth/login）提供用户名和密码输入表单。表单使用Flask-WTF生成，包含CSRF隐藏令牌。提交后验证凭据：调用User模型的check_password方法比对密码哈希值。验证通过后调用Flask-Login的login_user函数创建会话并重定向。界面设计包含系统Logo区域、登录表单卡片和注册链接。模板文件为auth/login.html，继承自layouts/base.html基础布局。')

    add_image_placeholder(doc, '[截图：登录界面]', '图3-4 用户登录界面')

    add_heading_text(doc, '3.5', '注册界面设计', level=2)
    add_body(doc, '注册界面（/auth/register）提供新用户注册表单，包含用户名、邮箱、密码和确认密码字段。表单验证规则包括：用户名长度2-64字符、邮箱格式校验（使用email-validator库）、密码长度至少6字符且与确认密码一致、用户名和邮箱唯一性数据库校验。注册成功后自动登录并重定向到用户首页。模板文件为auth/register.html。')

    add_image_placeholder(doc, '[截图：注册界面]', '图3-5 用户注册界面')

    add_heading_text(doc, '3.6', '管理后台首页设计', level=2)
    add_body(doc, '管理后台首页（/admin/dashboard）是管理员登录后的默认页面，提供系统运营数据的统计概览。页面顶部展示8个统计卡片：馆藏图书总数、注册用户总数、当前在借数量、逾期未还数量、图书分类数、待处理预约数、评论总数和累计罚金总额。页面下半部分展示最新借阅动态（最近10条）、最新评论（最近5条可见评论）和最新公告（最近5条已发布公告）。该页面在执行统计查询前会自动调用update_overdue_status()函数更新逾期状态。模板文件为admin/dashboard.html，继承自layouts/admin.html管理端布局。')

    add_image_placeholder(doc, '[截图：管理后台首页]', '图3-6 管理后台首页')

    add_heading_text(doc, '3.7', '图书管理界面设计', level=2)
    add_body(doc, '图书管理界面是管理员使用频率最高的功能模块，包含列表页（/admin/books）和表单页（/admin/books/add、/admin/books/<id>/edit）。列表页以表格形式展示所有图书，支持按书名/作者/ISBN进行模糊搜索，按分类下拉筛选，每页显示10条记录并提供分页导航。每条图书记录显示书名、作者、ISBN、分类、库存状态（可借数/总数）和操作按钮（详情/编辑/删除）。删除操作使用Bootstrap Modal确认弹窗，防止误操作，且删除前会检查是否存在未归还借阅记录。添加/编辑表单使用同一个模板文件（admin/book_form.html），通过传入不同的标题和预填数据来区分操作模式。表单字段包括书名、作者、ISBN、出版社、出版日期、分类（下拉选择）、总副本数、可借副本数、简介、馆藏位置和封面图片上传。')

    add_image_placeholder(doc, '[截图：图书管理列表]', '图3-7 图书管理列表界面')

    add_heading_text(doc, '3.8', '分类管理界面设计', level=2)
    add_body(doc, '分类管理界面（/admin/categories）将添加表单和分类列表集成在同一页面中。页面顶部为分类添加表单（名称+描述），下方为已有分类列表（表格展示）。每条分类支持内联编辑（通过POST请求更新名称和描述）和删除操作。删除分类前检查该分类下是否还有关联图书，有则提示无法删除。模板文件为admin/category_list.html。')

    add_image_placeholder(doc, '[截图：分类管理界面]', '图3-8 分类管理界面')

    add_heading_text(doc, '3.9', '借阅管理界面设计', level=2)
    add_body(doc, '借阅管理界面（/admin/borrows）展示所有借阅记录的列表，支持按状态筛选（全部/已借出/已归还/逾期）。每条记录显示借阅用户、图书名称、借阅日期、应还日期、归还日期、状态标签和罚金金额。状态标签使用不同颜色区分：绿色（已归还）、蓝色（已借出）、红色（逾期）。借书操作（/admin/borrows/add）通过搜索式表单选择用户和图书，后端自动校验库存和重复借阅。还书操作（/admin/borrows/<id>/return）通过POST请求触发，后端自动计算逾期天数和罚金，归还后检查是否有待处理预约。')

    add_image_placeholder(doc, '[截图：借阅管理界面]', '图3-9 借阅管理界面')

    add_heading_text(doc, '3.10', '用户图书浏览界面设计', level=2)
    add_body(doc, '用户图书浏览界面（/user/books）以卡片网格形式展示图书，每行显示3张卡片（桌面端），移动端自适应为1列。每张图书卡片包含封面图片（或默认占位图）、书名、作者和借阅状态标签（可借/已借完）。点击卡片进入图书详情页。页面顶部提供搜索框（按书名/作者）和分类筛选下拉菜单，支持分页（每页12条）。该界面的设计目标是提供直观、现代的浏览体验，引导读者发现和获取图书。模板文件为user/book_list.html，使用components/book_card.html组件渲染每一张卡片。')

    add_image_placeholder(doc, '[截图：用户图书浏览界面]', '图3-10 用户图书浏览界面')

    add_heading_text(doc, '3.11', '图书详情与评论界面设计', level=2)
    add_body(doc, '图书详情页（/user/books/<id>）是用户前台功能最丰富的页面。页面左侧展示图书封面大图，右侧展示完整书目信息（书名、作者、ISBN、出版社、出版日期、分类、馆藏位置、库存状态）。根据当前用户的借阅状态，动态显示不同的操作按钮：库存充足时显示"借阅"按钮；已借阅时显示"归还"按钮；库存为0时显示"预约"按钮；已预约时显示"已预约"标签。页面下半部分为评论区域：显示平均评分（星级展示）、评论数量统计和所有可见评论列表。用户若曾借阅过该图书且尚未评论，则显示评论提交表单（1-5星评分选择器+评论文本框）；若已发表评论，则显示自己的评论并支持修改。')

    add_image_placeholder(doc, '[截图：图书详情界面]', '图3-11 图书详情与评论界面')

    add_heading_text(doc, '3.12', '个人中心界面设计', level=2)
    add_body(doc, '个人中心界面（/user/profile）允许用户查看和编辑个人信息，包括用户名、邮箱和手机号。表单使用Flask-WTF进行验证，提交后更新数据库并刷新页面。个人中心页面还提供"修改密码"入口（/user/change-password），修改密码表单包含旧密码验证、新密码和确认新密码字段，验证旧密码正确后方可更新。模板文件为user/profile.html和user/change_password.html。')

    add_image_placeholder(doc, '[截图：个人中心界面]', '图3-12 个人中心界面')

    add_heading_text(doc, '3.13', '安全设计', level=2)
    add_body(doc, '系统在多个层面实施了安全防护措施。认证层面：密码使用Werkzeug的generate_password_hash函数（scrypt算法）进行哈希存储，不可逆；Flask-Login管理会话安全。授权层面：通过admin_required和role_required自定义装饰器实现基于角色的访问控制，非管理员访问管理路由返回403错误；用户操作（还书、取消预约、编辑个人信息）均验证操作者身份（current_user.id匹配记录所有者）。表单安全：Flask-WTF的CSRFProtect全局启用，所有POST请求均验证CSRF令牌。文件上传安全：使用secure_filename清洗文件名，UUID重命名防止路径遍历攻击。数据库安全：使用SQLAlchemy ORM的参数化查询，天然防止SQL注入攻击。')


# ============================================================
# Section 4: 系统测试
# ============================================================
def build_section4(doc):
    add_heading_text(doc, '4', '系统测试')

    add_body(doc, '系统测试采用黑盒测试方法，基于功能需求逐一验证各模块的正确性。以下选取8个核心功能场景的测试用例进行详细描述。')

    # Test case definition
    tests = [
        {
            'num': '4.1', 'title': '用户登录功能测试',
            'desc': '验证用户使用正确凭据登录系统，以及错误凭据被拒绝的情况。',
            'steps': [
                '1. 访问登录页面 /auth/login',
                '2. 输入正确的用户名"admin"和密码"admin123"',
                '3. 点击"登录"按钮',
                '4. 验证跳转至管理后台首页 /admin/dashboard',
                '5. 登出后尝试使用错误密码"wrong"登录',
                '6. 验证页面显示错误提示信息',
            ],
            'expected': '正确的用户名和密码组合能够成功登录并跳转到对应首页；错误的凭据被拒绝并显示提示信息。',
            'actual': '与预期一致，登录功能正常。'
        },
        {
            'num': '4.2', 'title': '用户注册功能测试',
            'desc': '验证新用户注册的数据验证逻辑。',
            'steps': [
                '1. 访问注册页面 /auth/register',
                '2. 输入用户名"testuser"、邮箱"test@example.com"、密码"123456"、确认密码"123456"',
                '3. 点击"注册"按钮',
                '4. 验证自动登录并跳转至用户首页',
                '5. 尝试使用相同用户名再次注册',
                '6. 验证系统提示"用户名已存在"错误',
            ],
            'expected': '使用新用户信息注册成功；重复用户名或邮箱被拒绝并给出明确提示。',
            'actual': '与预期一致，注册验证功能正常。'
        },
        {
            'num': '4.3', 'title': '图书添加与编辑功能测试',
            'desc': '验证管理员添加新图书和编辑已有图书的功能。',
            'steps': [
                '1. 以管理员身份登录，访问图书管理页面',
                '2. 点击"添加图书"，填写书名"测试图书"、作者"测试作者"等信息',
                '3. 上传封面图片文件',
                '4. 提交表单，验证列表页出现新添加的图书',
                '5. 点击该图书的"编辑"按钮，修改书名为"测试图书（修订版）"',
                '6. 提交修改，验证列表页书名已更新',
            ],
            'expected': '新书添加成功并显示在列表中；封面图片正确保存和显示；编辑操作更新数据正确。',
            'actual': '与预期一致，图书增改功能正常。'
        },
        {
            'num': '4.4', 'title': '图书借阅功能测试',
            'desc': '验证用户借阅图书的库存检查和状态更新逻辑。',
            'steps': [
                '1. 以普通用户身份登录，浏览图书列表',
                '2. 选择一本库存充足的图书，进入详情页',
                '3. 点击"借阅"按钮',
                '4. 验证跳转至"我的借阅"页面，新借阅记录显示状态为"已借出"',
                '5. 查看借阅日期和应还日期（应还日期 = 借阅日期 + 30天）',
                '6. 尝试再次借阅同一本图书，验证系统提示"已借阅"',
                '7. 查看该图书详情，验证可借库存已减1',
            ],
            'expected': '借阅操作成功后库存减少1，生成正确的借阅记录（含借阅日期和应还日期），重复借阅被拒绝。',
            'actual': '与预期一致，借阅功能正常。'
        },
        {
            'num': '4.5', 'title': '图书归还与罚金计算测试',
            'desc': '验证归还图书的库存恢复和逾期罚金自动计算功能。',
            'steps': [
                '1. 在"我的借阅"页面找到已借阅的记录',
                '2. 点击"归还"按钮确认归还',
                '3. 验证记录状态变为"已归还"，显示归还日期',
                '4. 查看该图书详情，验证可借库存已加1',
                '5. 对于逾期归还的记录（可通过修改数据库due_date模拟），验证罚金是否正确计算',
                '6. 逾期罚金 = 逾期天数 × 0.50元/天',
            ],
            'expected': '归还后库存正确恢复；正常归还无罚金；逾期归还按天数 × 0.50元正确计算罚金。',
            'actual': '与预期一致，归还与罚金计算功能正常。'
        },
        {
            'num': '4.6', 'title': '图书预约功能测试',
            'desc': '验证图书库存为0时的预约排队功能。',
            'steps': [
                '1. 找到一本库存为0的图书（可通过管理员添加库存为0的测试图书）',
                '2. 进入详情页，验证"预约"按钮显示',
                '3. 点击"预约"，验证预约记录创建成功',
                '4. 进入"我的预约"页面，验证预约记录状态为"待处理"',
                '5. 同一用户再次尝试预约同一图书，验证系统提示"已预约"',
                '6. 点击"取消预约"，验证记录状态变为"已取消"',
            ],
            'expected': '库存为0时用户可预约；同一用户对同一图书只能有一条待处理预约；取消预约功能正常。',
            'actual': '与预期一致，预约功能正常。'
        },
        {
            'num': '4.7', 'title': '评论发布功能测试',
            'desc': '验证用户对已借阅图书的评论和评分功能。',
            'steps': [
                '1. 选择一个曾经借阅过的图书，进入详情页',
                '2. 在评论区域选择4星评分，输入评论内容"这是一本好书"',
                '3. 点击"发表评论"',
                '4. 验证评论出现在详情页，显示4星评分和评论内容',
                '5. 修改评分为5星，修改内容为"非常推荐"',
                '6. 验证评论已更新',
            ],
            'expected': '借阅过的用户可发表评论；每位用户每本书只能有一条评论（更新而非新增）；评分和内容正确显示。',
            'actual': '与预期一致，评论功能正常。'
        },
        {
            'num': '4.8', 'title': '公告发布与管理测试',
            'desc': '验证管理员发布、编辑和上下架公告的功能。',
            'steps': [
                '1. 以管理员身份登录，访问公告管理页面',
                '2. 点击"发布公告"，填写标题"测试公告"、内容"这是一条测试公告"，选择优先级"重要"',
                '3. 提交表单，验证列表页出现新公告',
                '4. 在用户首页验证该公告显示在最新公告列表中',
                '5. 点击"下架"按钮，验证公告状态变为"未发布"',
                '6. 在用户首页验证该公告不再显示',
                '7. 点击"上架"按钮恢复发布状态',
            ],
            'expected': '公告发布后正确显示在用户首页；上下架操作切换发布状态；编辑和删除功能正常。',
            'actual': '与预期一致，公告管理功能正常。'
        },
    ]

    for test in tests:
        add_heading_text(doc, test['num'], test['title'], level=2)
        add_body(doc, test['desc'])
        add_table(doc,
            ['项目', '内容'],
            [
                ['测试步骤', test['steps'][0]],
                *[['', step] for step in test['steps'][1:]],
                ['预期结果', test['expected']],
                ['实际结果', test['actual']],
            ],
            col_widths=[Cm(2.0), Cm(10.0)]
        )


# ============================================================
# Section 5: 总结与展望
# ============================================================
def build_section5(doc):
    add_heading_text(doc, '5', '总结与展望')

    add_heading_text(doc, '5.1', '总结', level=2)
    add_body(doc, '通过本次课程设计，我成功完成了一个功能完整、架构清晰的Web图书管理系统。该系统基于Python Flask框架，采用MVC分层架构和蓝图（Blueprint）模块化设计，实现了用户认证、图书管理、借阅归还与逾期罚金计算、预约排队、评论评分和公告发布等核心业务功能。系统包含7个数据模型，4个功能蓝图模块，约50条路由处理函数，30余个Jinja2模板页面，以及约1100行自定义CSS样式代码，形成了一个较为完整的全栈Web应用。')
    add_body(doc, '在技术实践方面，我深入掌握了Flask框架的多个关键技术：应用工厂模式（create_app）实现了配置与代码的解耦；Flask-SQLAlchemy ORM简化了数据库操作并提供了天然的SQL注入防护；Flask-Login与自定义装饰器（admin_required）配合实现了灵活的认证与授权体系；Flask-WTF提供了便捷的表单验证和CSRF保护机制；Jinja2模板引擎的继承、包含和宏功能使得前端代码具有良好的可复用性。此外，通过实现借阅归还的库存联动、逾期状态的自动检测和罚金的动态计算等业务逻辑，加深了对数据库事务和业务规则设计的理解。')
    add_body(doc, '在项目实践中也遇到了一些技术挑战。例如，CSRF保护与AJAX请求的配合需要在每个异步请求中携带CSRF令牌；逾期状态的自动更新需要在多处查询点嵌入检测逻辑；借书和还书操作涉及多表更新，需要确保数据一致性；图书删除前需要检查关联数据。通过查阅官方文档和技术社区资源，这些问题都得到了妥善解决。')
    add_body(doc, '总的来说，本次课程设计不仅巩固了课堂所学的Web开发理论知识，还提升了独立解决实际开发问题的能力。从需求分析、数据库设计、前后端开发到系统测试的完整开发流程，让我对软件工程的生命周期有了更深入的理解和实践。')

    add_heading_text(doc, '5.2', '展望', level=2)
    add_body(doc, '虽然系统已经实现了图书管理的基本功能，但在以下几个方面仍有改进和扩展的空间：')
    add_body(doc, '第一，增加邮件通知功能。当用户的预约图书到馆时或借阅即将到期时，系统可以自动发送邮件提醒。这可以通过集成Flask-Mail扩展并在归还操作和定时任务中触发通知来实现。')
    add_body(doc, '第二，实现数据导出功能。管理员应能将图书列表、借阅记录、用户列表等数据导出为Excel或CSV格式，方便进行离线分析和报表制作。可使用openpyxl或pandas库实现表格数据的导出。')
    add_body(doc, '第三，增加条形码/ISBN扫码录入功能。在添加图书时，支持通过摄像头或扫码枪扫描ISBN条形码，自动从豆瓣API或Open Library API获取图书元数据，减少手动录入工作量。')
    add_body(doc, '第四，完善RESTful API接口。当前API仅提供搜索和统计功能，可扩展为完整的RESTful接口，支持前后端分离架构和移动端App的开发。可考虑使用Flask-RESTful或FastAPI进行重构。')
    add_body(doc, '第五，引入Docker容器化部署。编写Dockerfile和docker-compose.yml，将Flask应用、MySQL数据库和Nginx反向代理整合为容器化服务，简化部署流程和环境配置。')
    add_body(doc, '第六，增加操作审计日志。记录管理员的敏感操作（如删除图书、修改用户信息等），便于事后追溯和责任认定。可将日志存储到独立的数据库表或日志文件中。')


# ============================================================
# References
# ============================================================
def build_references(doc):
    add_heading_text(doc, '', '参考资料')
    add_blank_line(doc)

    refs = [
        '[1] Miguel Grinberg. Flask Web开发：基于Python的Web应用开发实战（第2版）[M]. 安道译. 人民邮电出版社, 2018.',
        '[2] 明日科技. Python Web从入门到精通（Django+Flask+项目实战）[M]. 清华大学出版社, 2021.',
        '[3] 李辉. Flask入门教程[EB/OL]. https://tutorial.helloflask.com/, 2025.',
        '[4] Adam Freeman. HTML5权威指南[M]. 谢廷晟等译. 人民邮电出版社, 2014.',
        '[5] Baron Schwartz, Peter Zaitsev, Vadim Tkachenko. 高性能MySQL（第4版）[M]. 宁海元等译. 电子工业出版社, 2022.',
        '[6] Bootstrap Team. Bootstrap 5.3 Documentation[EB/OL]. https://getbootstrap.com/docs/5.3/, 2024.',
        '[7] Pallets Projects. Flask Documentation (3.1.x)[EB/OL]. https://flask.palletsprojects.com/, 2025.',
        '[8] Pallets Projects. Jinja2 Template Engine Documentation[EB/OL]. https://jinja.palletsprojects.com/, 2025.',
        '[9] SQLAlchemy Authors. SQLAlchemy 2.0 Documentation[EB/OL]. https://docs.sqlalchemy.org/, 2025.',
        '[10] 刘胜超. UML在工业锅炉控制系统设计中的应用[J]. 华中科技大学学报, 2002, 30(4): 93-95.',
    ]

    from docx.oxml.ns import qn
    for ref in refs:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.left_indent = Cm(0.74)
        # Hanging indent for reference number
        run = p.add_run(ref)
        set_run_font(run, FONT_BODY, size=Pt(10.5))


# ============================================================
# Appendix
# ============================================================
def build_appendix(doc):
    add_heading_text(doc, '', '附  录')
    add_body(doc, '附录 源代码中写清楚注释信息，字号小四Times New Roman字体，格式层次要清晰。')

    # Appendix A: create_app
    code_a = """import os
from flask import Flask
from app.config import config_map
from app.extensions import db, migrate, login_manager, csrf


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(
        config_map.get(config_name, config_map['development'])
    )

    register_extensions(app)
    register_blueprints(app)
    register_commands(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    from app.auth import auth_bp
    from app.admin import admin_bp
    from app.user import user_bp
    from app.api import api_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(api_bp, url_prefix='/api')

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from flask import redirect, url_for
    from flask_login import current_user

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('user.dashboard'))
        return redirect(url_for('auth.login'))"""

    add_code_block(doc, code_a, '附录A：应用工厂函数 (app/__init__.py)')

    # Appendix B: Book model
    code_b = """from datetime import datetime
from app.extensions import db


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    isbn = db.Column(db.String(20), unique=True, nullable=True)
    publisher = db.Column(db.String(128), nullable=True)
    publish_date = db.Column(db.Date, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id',
                            ondelete='SET NULL'), nullable=True)
    total_copies = db.Column(db.Integer, nullable=False, default=1)
    available_copies = db.Column(db.Integer, nullable=False, default=1)
    cover_image = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(64), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    borrow_records = db.relationship('BorrowRecord', backref='book',
                                     lazy='dynamic')

    @property
    def is_available(self):
        return self.available_copies > 0"""

    add_code_block(doc, code_b, '附录B：图书模型 (app/models/book.py)')

    # Appendix C: BorrowRecord model
    code_c = """from datetime import datetime
from app.extensions import db


class BorrowRecord(db.Model):
    __tablename__ = 'borrow_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id',
                        ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id',
                        ondelete='CASCADE'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    return_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(16), nullable=False,
                       default='borrowed')
    fine = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    STATUS_BORROWED = 'borrowed'
    STATUS_RETURNED = 'returned'
    STATUS_OVERDUE = 'overdue'

    FINE_PER_DAY = 0.50

    @property
    def is_overdue(self):
        if self.status == self.STATUS_RETURNED:
            return False
        return datetime.utcnow() > self.due_date

    @property
    def overdue_days(self):
        if self.status == self.STATUS_RETURNED:
            if self.return_date and self.return_date > self.due_date:
                return (self.return_date - self.due_date).days
            return 0
        if datetime.utcnow() > self.due_date:
            return (datetime.utcnow() - self.due_date).days
        return 0

    def calculate_fine(self):
        return round(self.overdue_days * self.FINE_PER_DAY, 2)"""

    add_code_block(doc, code_c, '附录C：借阅记录模型 (app/models/borrow.py)')

    # Appendix D: admin_required decorator
    code_d = """from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated \
                or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated \
                    or current_user.role != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator"""

    add_code_block(doc, code_d, '附录D：权限装饰器 (app/decorators.py)')


# ============================================================
# Main
# ============================================================
def main():
    print('Generating report...')
    doc = Document()

    # Page setup
    setup_page(doc)
    setup_header_footer(doc)

    # Build all sections
    build_cover(doc)
    build_toc(doc)
    build_section1(doc)
    build_section2(doc)
    build_section3(doc)
    build_section4(doc)
    build_section5(doc)
    build_references(doc)
    build_appendix(doc)

    # Save
    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILENAME)
    doc.save(output_path)
    print(f'Report generated: {output_path}')
    print('Tip: Open with Word, right-click the TOC -> "Update Field" to populate it.')


if __name__ == '__main__':
    main()
