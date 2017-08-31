import os
from importlib.util import spec_from_file_location, module_from_spec

__dir__ = os.path.dirname(__file__)
sites = []

# 遍历当前文件目录并讲文件名和路径分开
l = [(l[:-3], os.path.join(__dir__, l)) for l in os.listdir(__dir__) if l != '__init__.py' and l.endswith('.py')]
for module_name, file_path in l:
    spec = spec_from_file_location(module_name, file_path)
    m = module_from_spec(spec)  # 从文件中加载模块
    spec.loader.exec_module(m)
    if getattr(m, 'Site', None):
        sites.append(m.Site)
