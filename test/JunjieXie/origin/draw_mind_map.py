from pyvis.network import Network

# 创建一个网络图
net = Network()

# 添加节点
net.add_node(1, label="Root")
net.add_node(2, label="Child 1")
net.add_node(3, label="Child 2")
net.add_node(4, label="Subchild 1")
net.add_node(5, label="Subchild 2")

# 添加边
net.add_edge(1, 2)
net.add_edge(1, 3)
net.add_edge(2, 4)
net.add_edge(3, 5)

# 生成交互式HTML文件
net.force_atlas_2based(gravity=-10)
net.show("mind_map.html")
