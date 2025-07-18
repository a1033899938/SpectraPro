from pptx import Presentation
from pptx.util import Pt, Emu
from pptx.oxml import parse_xml
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_SHAPE_TYPE  # 导入形状类型枚举

# 创建PPT对象
prs = Presentation()
slide = prs.slides.add_slide(prs.slide_layouts[5])
slide.shapes.title.text = "模仿手动创建的贝塞尔曲线"

# 解析XML中的路径数据（根据你的slide1.xml提取）
shape_left_emu = 3634596  # EMU，手动提取自XML: <a:off x="3634596" y="3443760"/>
shape_top_emu = 3443760
shape_width_emu = 3082506  # EMU, <a:ext cx="3082506" cy="1802398"/>
shape_height_emu = 1802398

# 将EMU转换为Length对象
shape_left = Emu(shape_left_emu)
shape_top = Emu(shape_top_emu)
shape_width = Emu(shape_width_emu)
shape_height = Emu(shape_height_emu)

# 路径数据（从<a:pathLst>提取，确保XML格式正确）
path_xml = '''
<a:path xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" 
        a:w="3082506" 
        a:h="1802398">
    <a:moveTo>
        <a:pt a:x="0" a:y="1024723"/>
    </a:moveTo>
    <a:cubicBezTo>
        <a:pt a:x="159110" a:y="498991"/>
        <a:pt a:x="318220" a:y="-26741"/>
        <a:pt a:x="477329" a:y="1055"/>
    </a:cubicBezTo>
    <!-- 省略其他曲线段，保持与原XML一致 -->
    <a:cubicBezTo>
        <a:pt a:x="3082506" a:y="369115"/>
    </a:cubicBezTo>
</a:path>
'''

# 创建任意多边形形状（类型码为10，对应MSO_SHAPE_TYPE.FREEFORM）
shape = slide.shapes.add_shape(
    MSO_SHAPE_TYPE.FREEFORM,  # 位置参数，指定形状类型
    shape_left,
    shape_top,
    shape_width,
    shape_height
)

# 获取形状的底层XML元素
sp = shape._element
spPr = sp.find(qn('p:spPr'))

# 移除默认几何图形（如果存在）
for child in spPr:
    if child.tag.endswith('}prstGeom'):
        spPr.remove(child)
        break

# 添加自定义路径
path_lst = parse_xml('<a:pathLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
path_lst.append(parse_xml(path_xml))

# 添加线条样式（修正后的XML格式）
ln = parse_xml('''
<a:ln xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" 
    a:w="34335" a:cap="rnd" a:cmpd="sng" a:algn="ctr">
    <a:solidFill>
        <a:srgbClr a:val="FF0000"/>
    </a:solidFill>
    <a:prstDash val="solid"/>
</a:ln>
''')
spPr.append(ln)

# 添加无填充样式
no_fill = parse_xml('<a:noFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"/>')
spPr.append(no_fill)

# 添加路径列表到spPr
spPr.append(path_lst)

# 保存PPT
prs.save("imitated_bezier_shape.pptx")
print("已生成模仿的贝塞尔曲线形状PPT！")