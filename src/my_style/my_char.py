class My_Char:
    """
    希腊字母（常称“罗马字符”）工具类，返回对应Unicode字符
    包含全部24个希腊字母的大小写，及常用变体
    """
    greek_chars = {
        # 第一组：α β γ δ ε ζ η θ ι κ λ μ ν
        'alpha': ('\u03B1', '\u0391'),
        'beta': ('\u03B2', '\u0392'),
        'gamma': ('\u03B3', '\u0393'),
        'delta': ('\u03B4', '\u0394'),
        'epsilon': ('\u03B5', '\u0395'),
        'zeta': ('\u03B6', '\u0396'),
        'eta': ('\u03B7', '\u0397'),
        'theta': ('\u03B8', '\u0398'),
        'iota': ('\u03B9', '\u0399'),
        'kappa': ('\u03BA', '\u039A'),
        'lambda': ('\u03BB', '\u039B'),
        'mu': ('\u03BC', '\u039C'),
        'nu': ('\u03BD', '\u039D'),

        # 第二组：ξ ο π ρ σ τ υ φ χ ψ ω
        'xi': ('\u03BE', '\u039E'),
        'omicron': ('\u03BF', '\u039F'),
        'pi': ('\u03C0', '\u03A0'),
        'rho': ('\u03C1', '\u03A1'),
        'sigma': ('\u03C3', '\u03A3'),  # 小写σ，变体ς（终末sigma）：\u03C2
        'tau': ('\u03C4', '\u03A4'),  # 重点：tau（τ/Τ）
        'upsilon': ('\u03C5', '\u03A5'),
        'phi': ('\u03C6', '\u03A6'),
        'chi': ('\u03C7', '\u03A7'),
        'psi': ('\u03C8', '\u03A8'),
        'omega': ('\u03C9', '\u03A9'),

        # 扩展：常用变体/特殊形式
        'sigma_final': ('\u03C2', None),  # 终末sigma（ς），无大写
        'varpi': ('\u03D6', '\u03D6'),  # 变体pi（ϖ）
        'vartheta': ('\u03D1', '\u03D1'),  # 变体theta（ϑ）
        'varphi': ('\u03D5', '\u03D5')  # 变体phi（φ/ϕ）
    }

    @classmethod
    def get(cls, character):
        """
        根据字符名称（小写）返回对应希腊字母Unicode字符
        :param character: 字母名称（如tau、alpha，小写）
        :return: 对应希腊字母字符（小写/大写），未找到返回None
        """
        # 核心：希腊字母名称 → (小写Unicode, 大写Unicode) 映射表

        first_char = character[0]
        idx = 0 if first_char.islower() else 1

        lower_char_key = character.lower()


        if lower_char_key in cls.greek_chars:
            return cls.greek_chars[lower_char_key][idx]

        return None

    # 扩展方法：批量获取/验证（可选）
    @classmethod
    def get_all(cls):
        """返回所有希腊字母名称+大小写字符的字典"""
        all_chars = {}
        for name, (lower, upper) in cls.greek_chars.items():
            all_chars[name] = {'lower': lower, 'upper': upper}
        return all_chars


# ==================== 使用示例 ====================
if __name__ == "__main__":
    roman = My_Char()
    
    # 1. 获取小写tau（τ）
    print(roman.get('tau'))          # 输出：τ
    
    # 2. 获取大写tau（Τ）
    print(roman.get('Tau'))    # 输出：Τ
    
    # 3. 获取其他字母（示例）
    print(roman.get('alpha'))        # 输出：α
    print(roman.get('Alpha'))  # 输出：Α
    print(roman.get('sigma'))        # 输出：σ
    print(roman.get('Sigma'))  # 输出：ς
    print(roman.get('pi'))           # 输出：π
    print(roman.get('varphi'))        # 输出：ϖ
    
    # 4. 无效输入返回None
    print(roman.get('invalid'))      # 输出：None