
#%%
from collections import defaultdict
import os


#%%
def analyze_assembly_file(file_path):
    """
    分析assembly.txt文件，统计偏旁和按键的对应关系
    格式：字[Tab]偏旁[空格][空格]|[空格][空格]按键
    文件编码：UTF-8 with BOM
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"错误: 文件 '{file_path}' 不存在")
        print(f"当前目录: {os.getcwd()}")
        return None
    
    # 统计字典
    radical_to_keys = defaultdict(set)   # 偏旁 -> 按键集合
    key_to_radicals = defaultdict(set)   # 按键 -> 偏旁集合
    radical_to_chars = defaultdict(list) # 偏旁 -> 汉字列表
    key_to_chars = defaultdict(list)     # 按键 -> 汉字列表
    
    # 使用 utf-8-sig 编码自动处理 BOM
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            content = f.read()
        print(f"✓ 成功使用 UTF-8 with BOM 编码读取文件")
    except Exception as e:
        print(f"✗ 读取文件时出错: {e}")
        return None
    
    lines = content.split('\n')
    print(f"文件共 {len(lines)} 行\n")
    
    # 显示前几行内容用于调试
    print("前5行原始内容:")
    for i, line in enumerate(lines[:5], 1):
        if line.strip():
            print(f"  第{i}行: {repr(line[:50])}")
    print()
    
    # 解析每一行
    success_count = 0
    line_num = 0
    for line in lines:
        line_num+=1
        line = line.strip()
        if not line:
            continue
        
        # 按 tab 分割
        if '\t' not in line:
            print(f"第{line_num}行: 没有找到tab分隔符 - {repr(line)}")
            continue
        
        # 分割成左右两部分
        left_part, right_part = line.split('\t', 1)
        
        # 提取汉字（左边第一个字符）
        if not left_part:
            print(f"第{line_num}行: 左边部分为空")
            continue
        char = left_part[0]
        

        
        # 从右边部分提取按键
        # 格式是 "⺈  |  F "，需要去掉 "| " 和前后空格
        # 提取偏旁（左边剩余部分，去掉多余空格）
        radical = right_part.split('|')[0].strip()
        key_part = right_part.split('|')[-1].strip()
        key = key_part.strip()
        
        # 验证提取的数据
        if not char or not radical or not key:
            print(f"第{line_num}行: 数据不完整 - 字='{char}' 偏旁='{radical}' 按键='{key}'")
            continue
        
        # 统计
        radical_to_keys[radical].add(key)
        key_to_radicals[key].add(radical)
        radical_to_chars[radical].append(char)
        key_to_chars[key].append(char)
        success_count += 1
        
        # 显示前几行的解析结果
        if line_num <= 3:
            print(f"第{line_num}行解析: 字='{char}' 偏旁='{radical}' 按键='{key}'")
    
    print(f"\n成功解析 {success_count} 行数据\n")
    
    return radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars

def print_statistics(radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars):
    """打印统计结果"""
    print("=" * 70)
    print("按偏旁统计：")
    print("=" * 70)
    for radical in sorted(radical_to_keys.keys()):
        keys = sorted(radical_to_keys[radical])
        chars = radical_to_chars[radical]
        print(f"偏旁 '{radical}' -> 按键 {keys}")
        print(f"  对应汉字 ({len(chars)}个): {' '.join(chars)}")
        print()
    
    print("=" * 70)
    print("按按键统计：")
    print("=" * 70)
    for key in sorted(key_to_radicals.keys()):
        radicals = sorted(key_to_radicals[key])
        chars = key_to_chars[key]
        print(f"按键 '{key}' -> 偏旁 {radicals}")
        print(f"  对应汉字 ({len(chars)}个): {' '.join(chars)}")
        print()

def save_statistics(radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars, output_file="统计结果.txt"):
    """保存统计结果到文件"""
    with open(output_file, 'w', encoding='utf-8-sig') as f:
        f.write("按偏旁统计：\n")
        f.write("=" * 70 + "\n")
        for radical in sorted(radical_to_keys.keys()):
            keys = sorted(radical_to_keys[radical])
            chars = radical_to_chars[radical]
            f.write(f"偏旁 '{radical}' -> 按键 {keys}\n")
            f.write(f"  对应汉字 ({len(chars)}个): {' '.join(chars)}\n\n")
        
        f.write("\n" + "=" * 70 + "\n")
        f.write("按按键统计：\n")
        f.write("=" * 70 + "\n")
        for key in sorted(key_to_radicals.keys()):
            radicals = sorted(key_to_radicals[key])
            chars = key_to_chars[key]
            f.write(f"按键 '{key}' -> 偏旁 {radicals}\n")
            f.write(f"  对应汉字 ({len(chars)}个): {' '.join(chars)}\n\n")
    
    print(f"统计结果已保存到 '{output_file}'")

#%% 使用示例
file_path = r"D:\RIME_config\lua\pdbj\assembly.txt"  # 修改为你的文件路径

print(f"开始分析文件: {file_path}\n")

result = analyze_assembly_file(file_path)

if result:
    radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars = result
    print_statistics(radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars)
    #save_statistics(radical_to_keys, key_to_radicals, radical_to_chars, key_to_chars)
else:
    print("分析失败，请检查文件路径和格式")

# %% 重新映射新代码：
from collections import defaultdict

def map_radicals_to_keys(new_file_path, radical_to_keys, output_file="映射结果.txt"):
    """
    根据偏旁到按键的映射，把新文件中的偏旁转换为按键
    
    参数:
        new_file_path: 新文件的路径（格式：字\t偏旁）
        radical_to_keys: 偏旁到按键的映射字典 {偏旁: {按键集合}}
        output_file: 输出文件路径
    """
    # 结果字典
    char_to_key = {}
    char_to_radical = {}
    
    # 按键统计
    key_to_chars = defaultdict(list)
    
    # 读取新文件（UTF-8 BOM编码）
    try:
        with open(new_file_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
        print(f"✓ 成功读取文件: {new_file_path}")
        print(f"  共 {len(lines)} 行\n")
    except Exception as e:
        print(f"✗ 读取文件失败: {e}")
        return None
    
    # 解析并映射
    success_count = 0
    no_mapping_count = 0
    
    for line_num, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue
        
        # 按 tab 分割
        if '\t' not in line:
            print(f"第{line_num}行: 没有找到tab分隔符 - {repr(line)}")
            continue
        
        char, radical = line.split('\t', 1)
        char = char.strip()
        radical = radical.strip()
        
        # 查找对应的按键
        if radical in radical_to_keys:
            keys = radical_to_keys[radical]
            # 如果有多个按键，取第一个（按字母排序）
            key = sorted(keys)[0] if keys else ""
            
            if key:
                char_to_key[char] = key
                char_to_radical[char] = radical
                key_to_chars[key].append(char)
                success_count += 1
                
                # 显示前几行结果
                if line_num <= 5:
                    print(f"第{line_num}行映射: 字='{char}' 偏旁='{radical}' -> 按键='{key}'")
            else:
                print(f"第{line_num}行: 偏旁 '{radical}' 没有对应的按键")
                no_mapping_count += 1
        else:
            print(f"第{line_num}行: 偏旁 '{radical}' 未在映射表中找到")
            no_mapping_count += 1
    
    print(f"\n映射完成:")
    print(f"  成功映射: {success_count} 个")
    print(f"  未找到映射: {no_mapping_count} 个\n")
    
    # 保存结果
    if char_to_key:
        with open(output_file, 'w', encoding='utf-8-sig') as f:
            f.write("字\t偏旁 || 按键\n")
            f.write("=" * 50 + "\n")
            
            # 按按键分组显示
            for key in sorted(key_to_chars.keys()):
                chars = key_to_chars[key]
                for char in chars:
                    radical = char_to_radical[char]
                    f.write(f"{char}\t{radical}  |  {key}\n")
            
            # f.write("\n" + "=" * 50 + "\n")
            # f.write("按按键分组:\n")
            # f.write("=" * 50 + "\n")
            # for key in sorted(key_to_chars.keys()):
            #     chars = key_to_chars[key]
            #     f.write(f"按键 '{key}': {' '.join(chars)}\n")
        
        print(f"✓ 结果已保存到 '{output_file}'")
    
    return char_to_key, char_to_radical, key_to_chars

#%% 使用示例

# 你的新文件路径
new_file_path = r"G:\OneDrive - csu.edu.cn\重要软件备份\输入法\拼读并击250412\lua\pdbj\assembly.txt"  # 修改为你的实际文件路径

# 使用之前统计得到的 radical_to_keys
# 如果你有完整的 radical_to_keys，直接使用即可
# radical_to_keys #= {'⺈': {'F'}, '⺌': {'T'}, '八': {'S'}}  # 示例数据，替换成你的实际数据

print("=" * 60)
print("开始偏旁到按键的映射")
print("=" * 60 + "\n")

result = map_radicals_to_keys(new_file_path, radical_to_keys, "E:\Downloads\映射结果.txt")

if result:
    char_to_key, char_to_radical, key_to_chars = result
    
    print("\n" + "=" * 60)
    print("按按键分组的结果:")
    print("=" * 60)
    for key in sorted(key_to_chars.keys()):
        chars = key_to_chars[key]
        print(f"按键 '{key}': {' '.join(chars)}")


# %%
radical_to_keys = defaultdict(set,
            {'⺊':{'S'},
             '匕':{'QF/QS'},
             '耳':{'R'},
             '阝':{'R'},
             '虎':{'ZV'},
             '耂':{'B'},
             '朩':{'D'},
             '𦍌':{'F'},
             '入':{'R'},
             '氺':{'CZ'},
             '巳':{'B'},
             '㔾':{'WQ'},
             '㣺':{'XZ'},
             '爫':{'E'},
             '龵':{'C'},

             '⺈': {'F'},
             '⺌': {'T'},
             '八': {'S'},
             '丷': {'S'},
             '白': {'S'},
             '勹': {'S'},
             '宀': {'Q'},
             '贝': {'S'},
             '鼻': {'QF'},
             '髟': {'QF'},
             '疒': {'QF'},
             '卜': {'S'},
             '不': {'S'},
             '艹': {'CD'},
             '刂': {'F'},
             '厂': {'DS'},
             '车': {'DS'},
             '齿': {'DS'},
             '彳': {'DS'},
             '赤': {'DS'},
             '虫': {'DA'},
             '巛': {'DA'},
             '寸': {'DA'},
             '大': {'F'},
             '歹': {'F'},
             '亻': {'I'},
             '卩': {'W'},
             '刀': {'F'},
             '丶': {'FE'},
             '斗': {'F'},
             '豆': {'F'},
             '儿': {'R'},
             '而': {'R'},
             '二': {'R'},
             '犭': {'SG'},
             '攵': {'X'},
             '匚': {'AF'},
             '方': {'C'},
             '非': {'C'},
             '风': {'C'},
             '缶': {'C'},
             '父': {'C'},
             '阜': {'C'},
             '戈': {'Q'},
             '革': {'Q'},
             '鬲': {'Q'},
             '艮': {'Q'},
             '工': {'QR'},
             '弓': {'QR'},
             '廾': {'CD'},
             '谷': {'QR'},
             '骨': {'QR'},
             '瓜': {'QR'},
             '广': {'QR'},
             '鬼': {'QR'},
             '禾': {'Z'},
             '黑': {'Z'},
             '虍': {'ZV'},
             '户': {'ZV'},
             '火': {'ZV'},
             '灬': {'ZV'},
             '几': {'W'},
             '己': {'W'},
             '彐': {'XB'},
             '见': {'W'},
             '纟': {'M'},
             '角': {'W'},
             '巾': {'W'},
             '斤': {'W'},
             '钅': {'H'},
             '金': {'W'},
             '臼': {'W'},
             '口': {'AG'},
             '老': {'B'},
             '耒': {'B'},
             '力': {'BF'},
             '立': {'BF'},
             '冫': {'QF'},
             '龙': {'BD'},
             '鹿': {'BD'},
             '马': {'D'},
             '毛': {'D'},
             '矛': {'D'},
             '门': {'D'},
             '米': {'DW'},
             '糸': {'SR'},
             '皿': {'DW'},
             '母': {'D'},
             '木': {'J'},
             '目': {'D'},
             '鸟': {'GR'},
             '牛': {'GR'},
             '女': {'GW'},
             '皮': {'AV/XA'},
             '片': {'AV/XA'},
             '丿': {'AV/XA'},
             '冖': {'DW'},
             '气': {'SA'},
             '凵': {'AF'},
             '欠': {'SA'},
             '犬': {'SG'},
             '人': {'RE'},
             '日': {'RE'},
             '肉': {'RE'},
             '三': {'B'},
             '彡': {'C'},
             '氵': {'K'},
             '山': {';'},
             '舌': {'C'},
             '身': {'C'},
             '尸': {'C'},
             '十': {'C'},
             '饣': {'C'},
             '石': {'L'},
             '食': {'A'},
             '矢': {'A'},
             '豕': {'A'},
             '士': {'A'},
             '礻': {'A'},
             '示': {'A'},
             '手': {'A'},
             '首': {'A'},
             '殳': {'CZ'},
             '鼠': {'CZ'},
             '丨': {'CZ'},
             '忄': {'P'},
             '水': {'CZ'},
             '厶': {'SR'},
             '罒': {'SR'},
             '夊': {'X'},
             '扌': {'U'},
             '田': {'VD'},
             '冂': {'AF'},
             '土': {'VS'},
             '瓦': {'VC'},
             '王': {'VC'},
             '囗': {'AF'},
             '韦': {'VC'},
             '亠': {'V'},
             '文': {'V'},
             '夕': {'T'},
             '覀': {'T'},
             '香': {'T'},
             '小': {'T'},
             '心': {'T'},
             '辛': {'T'},
             '行': {'T'},
             '穴': {'XB'},
             '血': {'XB'},
             '牙': {'FD'},
             '讠': {'O'},
             '言': {'FD'},
             '羊': {'FD'},
             '业': {'FD'},
             '页': {'Y'},
             '一': {'Z'},
             '衤': {'<'},
             '衣': {'FD'},
             '邑': {'N'},
             '音': {'FD'},
             '廴': {'FD'},
             '用': {'FS'},
             '尢': {'FD'},
             '酉': {'FD'},
             '又': {'FD'},
             '鱼': {'>'},
             '羽': {'FS'},
             '雨': {'FS'},
             '玉': {'FS'},
             '聿': {'FS'},
             '月': {'FS'},
             '爪': {'EQ'},
             '乛': {'E'},
             '支': {'E'},
             '止': {'E'},
             '豸': {'E'},
             '舟': {'E'},
             '竹': {'EQ'},
             '隹': {'EQ'},
             '子': {'ZF'},
             '辶': {'ZF'},
             '走': {'ZF'},
             '足': {'ZD'}})
# %%
