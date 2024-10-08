class MyClass:
    class_variable = 0  # 类属性

    def __init__(self, value):
        self.value = value  # 实例属性
        MyClass.class_variable += 1  # 每次创建实例时，增加类属性

    # 实例方法
    def instance_method(self):
        print(f"Instance method called. Value is {self.value}")

    # 类方法
    @classmethod
    def class_method(cls):
        print(f"Class method called. Class variable is {cls.class_variable}")

    # 静态方法
    @staticmethod
    def static_method():
        print("Static method called. It does not depend on class or instance.")

# 创建实例
obj1 = MyClass(10)
obj2 = MyClass(20)

# 调用实例方法（通过实例调用）
obj1.instance_method()  # 输出：Instance method called. Value is 10
obj2.instance_method()  # 输出：Instance method called. Value is 20

# 调用类方法（通过类调用）
MyClass.class_method()  # 输出：Class method called. Class variable is 2

# 调用类方法（通过实例调用）
obj1.class_method()  # 输出：Class method called. Class variable is 2

# 调用静态方法（通过类调用）
MyClass.static_method()  # 输出：Static method called. It does not depend on class or instance.

# 调用静态方法（通过实例调用）
obj1.static_method()  # 输出：Static method called. It does not depend on class or instance.


# 单行注释

"""
多行注释
多行注释
多行注释
"""