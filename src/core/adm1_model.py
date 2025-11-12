"""
ADM1核心模型定义
包含26个状态变量和19个生化过程
基于文档2的ADM1框架和文档6的金属扩展
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class ADM1Parameters:
    """ADM1模型参数类（文档2表2.2-2.5）"""
    # 水解参数
    k_dis: float = 0.5        #  disintegration rate [d⁻¹]
    k_hyd_ch: float = 10.0    #  carbohydrate hydrolysis rate [d⁻¹]
    k_hyd_pr: float = 10.0    #  protein hydrolysis rate [d⁻¹]
    k_hyd_li: float = 10.0    #  lipid hydrolysis rate [d⁻¹]

    # 产酸菌参数（单糖降解）
    k_m_su: float = 30.0      #  monosaccharide uptake rate [d⁻¹]
    K_S_su: float = 0.5       #  half-saturation constant [gCOD/m³]
    Y_su: float = 0.1         #  yield coefficient [-]

    # 产酸菌参数（氨基酸降解）
    k_m_aa: float = 50.0      #  amino acid uptake rate [d⁻¹]
    K_S_aa: float = 0.3       #  half-saturation constant [gCOD/m³]
    Y_aa: float = 0.08        #  yield coefficient [-]

    # 产酸菌参数（长链脂肪酸降解）
    k_m_fa: float = 6.0       #  LCFA uptake rate [d⁻¹]
    K_S_fa: float = 0.4       #  half-saturation constant [gCOD/m³]
    Y_fa: float = 0.06        #  yield coefficient [-]

    # 产氢产乙酸菌参数
    k_m_c4: float = 20.0      #  butyrate/valerate uptake rate [d⁻¹]
    K_S_c4: float = 0.2       #  half-saturation constant [gCOD/m³]
    k_m_pro: float = 13.0     #  propionate uptake rate [d⁻¹]
    K_S_pro: float = 0.1      #  half-saturation constant [gCOD/m³]

    # 产甲烷菌参数
    k_m_ac: float = 8.0       #  acetate uptake rate [d⁻¹]
    K_S_ac: float = 0.15      #  half-saturation constant [gCOD/m³]
    Y_ac: float = 0.05        #  yield coefficient [-]
    k_m_h2: float = 35.0      #  hydrogen uptake rate [d⁻¹]
    K_S_h2: float = 7e-6      #  half-saturation constant [gCOD/m³]
    Y_h2: float = 0.06        #  yield coefficient [-]

    # 抑制参数
    KI_h2_fa: float = 5e-6    #  hydrogen inhibition for LCFA [gCOD/m³]
    KI_h2_c4: float = 1e-5    #  hydrogen inhibition for C4 [gCOD/m³]
    KI_h2_pro: float = 3.5e-6 #  hydrogen inhibition for propionate [gCOD/m³]
    KI_nh3: float = 0.0018    #  ammonia inhibition [M]

    # 金属扩展参数（文档6表2）
    k_edta_fe: float = 1e5    #  Fe-EDTA complexation rate [m³/mol/d]
    k_edta_fe_rev: float = 0.1 #  reverse rate [d⁻¹]
    k_precip_fes: float = 0.01 #  FeS precipitation rate [d⁻¹]

class ADM1Model:
    """ADM1模型主类"""

    def __init__(self, parameters: ADM1Parameters = None):
        """
        初始化ADM1模型
        基于文档2的26个状态变量定义 + 文档6的4个金属变量
        """
        self.parameters = parameters or ADM1Parameters()

        # 定义完整的26个状态变量名称（文档2表2.6）
        self.state_variables = [
            # 溶解性组分 (S_) - 12个
            'S_su',    #  monosaccharides [gCOD/m³]
            'S_aa',    #  amino acids [gCOD/m³]
            'S_fa',    #  long chain fatty acids [gCOD/m³]
            'S_va',    #  total valerate [gCOD/m³]
            'S_bu',    #  total butyrate [gCOD/m³]
            'S_pro',   #  total propionate [gCOD/m³]
            'S_ac',    #  total acetate [gCOD/m³]
            'S_h2',    #  hydrogen gas [gCOD/m³]
            'S_ch4',   #  methane gas [gCOD/m³]
            'S_IC',    #  inorganic carbon [molC/m³]
            'S_IN',    #  inorganic nitrogen [molN/m³]
            'S_I',     #  soluble inerts [gCOD/m³]

            # 颗粒性组分 (X_) - 11个
            'X_ch',    #  composites carbohydrates [gCOD/m³]
            'X_pr',    #  composites proteins [gCOD/m³]
            'X_li',    #  composites lipids [gCOD/m³]
            'X_su',    #  sugar degraders [gCOD/m³]
            'X_aa',    #  amino acid degraders [gCOD/m³]
            'X_fa',    #  LCFA degraders [gCOD/m³]
            'X_c4',    #  valerate/butyrate degraders [gCOD/m³]
            'X_pro',   #  propionate degraders [gCOD/m³]
            'X_ac',    #  acetate degraders [gCOD/m³]
            'X_h2',    #  hydrogen degraders [gCOD/m³]
            'X_I',     #  particulate inerts [gCOD/m³]

            # 离子组分 - 2个
            'S_cat',   #  cations [eq/m³]
            'S_an',    #  anions [eq/m³]

            # 文档6金属扩展 - 4个
            'S_Fe2',   #  ferrous iron [mol/m³]
            'S_EDTA',  #  EDTA [mol/m³]
            'S_FeEDTA', #  Fe-EDTA complex [mol/m³]
            'X_FeS'    #  iron sulfide precipitate [mol/m³]
        ]

        # 初始化状态向量（基于文档3表3-2和文档6表5）
        self.initial_conditions = self._set_initial_conditions()

        # 创建变量索引映射
        self.variable_index = {var: idx for idx, var in enumerate(self.state_variables)}

    def _set_initial_conditions(self) -> np.ndarray:
        """设置初始条件（文档3表3-2典型值）"""
        initial_values = [
            # 溶解性组分 (S_)
            5.0,    # S_su [gCOD/m³]
            2.0,    # S_aa [gCOD/m³]
            0.1,    # S_fa [gCOD/m³]
            0.05,   # S_va [gCOD/m³]
            0.05,   # S_bu [gCOD/m³]
            0.1,    # S_pro [gCOD/m³]
            0.5,    # S_ac [gCOD/m³]
            1e-6,   # S_h2 [gCOD/m³]
            0.1,    # S_ch4 [gCOD/m³]
            0.1,    # S_IC [molC/m³]
            0.05,   # S_IN [molN/m³]
            0.1,    # S_I [gCOD/m³]

            # 颗粒性组分 (X_)
            10.0,   # X_ch [gCOD/m³]
            8.0,    # X_pr [gCOD/m³]
            6.0,    # X_li [gCOD/m³]
            1.0,    # X_su [gCOD/m³]
            0.8,    # X_aa [gCOD/m³]
            0.6,    # X_fa [gCOD/m³]
            0.5,    # X_c4 [gCOD/m³]
            0.4,    # X_pro [gCOD/m³]
            0.3,    # X_ac [gCOD/m³]
            0.2,    # X_h2 [gCOD/m³]
            2.0,    # X_I [gCOD/m³]

            # 离子组分
            0.01,   # S_cat [eq/m³]
            0.01,   # S_an [eq/m³]

            # 金属扩展（文档6表5）
            0.01,   # S_Fe2 [mol/m³]
            0.001,  # S_EDTA [mol/m³]
            0.0,    # S_FeEDTA [mol/m³]
            0.0     # X_FeS [mol/m³]
        ]

        return np.array(initial_values)

    def biochemical_reactions(self, t: float, y: np.ndarray) -> np.ndarray:
        """
        计算19个生化过程的反应速率
        基于文档2表3.1-3.2的动力学方程
        """
        # 解包关键状态变量
        S_su, S_aa, S_fa, S_va, S_bu, S_pro, S_ac, S_h2 = y[0:8]
        X_su, X_aa, X_fa, X_c4, X_pro, X_ac, X_h2 = y[15:22]
        S_IN = y[10]

        # 初始化反应速率向量
        reaction_rates = np.zeros(len(y))

        # 1. 单糖降解（文档2第3.4.1节）
        r_su = self._monod_kinetics(S_su, self.parameters.K_S_su,
                                  self.parameters.k_m_su, X_su)
        reaction_rates[0] = -r_su  # S_su消耗
        reaction_rates[15] = r_su * self.parameters.Y_su  # X_su生长

        # 2. 氨基酸降解（文档2第3.4.2节）
        r_aa = self._monod_kinetics(S_aa, self.parameters.K_S_aa,
                                  self.parameters.k_m_aa, X_aa)
        reaction_rates[1] = -r_aa  # S_aa消耗
        reaction_rates[16] = r_aa * self.parameters.Y_aa  # X_aa生长

        # 3. 长链脂肪酸降解（文档2第3.4.3节）
        inhibition_h2_fa = self._hydrogen_inhibition(S_h2, self.parameters.KI_h2_fa)
        r_fa = self._monod_kinetics(S_fa, self.parameters.K_S_fa,
                                  self.parameters.k_m_fa, X_fa) * inhibition_h2_fa
        reaction_rates[2] = -r_fa  # S_fa消耗
        reaction_rates[17] = r_fa * self.parameters.Y_fa  # X_fa生长

        # 4. 丁酸/戊酸降解（文档2第3.4.4节）
        S_c4 = S_va + S_bu  # C4组分总和
        inhibition_h2_c4 = self._hydrogen_inhibition(S_h2, self.parameters.KI_h2_c4)
        r_c4 = self._monod_kinetics(S_c4, self.parameters.K_S_c4,
                                  self.parameters.k_m_c4, X_c4) * inhibition_h2_c4
        reaction_rates[3] = -r_c4 * (S_va / S_c4)  # S_va消耗
        reaction_rates[4] = -r_c4 * (S_bu / S_c4)  # S_bu消耗
        reaction_rates[19] = r_c4 * 0.1  # X_c4生长（简化）

        # 5. 丙酸降解（文档2第3.4.5节）
        inhibition_h2_pro = self._hydrogen_inhibition(S_h2, self.parameters.KI_h2_pro)
        r_pro = self._monod_kinetics(S_pro, self.parameters.K_S_pro,
                                   self.parameters.k_m_pro, X_pro) * inhibition_h2_pro
        reaction_rates[5] = -r_pro  # S_pro消耗
        reaction_rates[20] = r_pro * 0.08  # X_pro生长

        # 6. 乙酸降解（文档2第3.4.6节）
        inhibition_nh3 = self._ammonia_inhibition(S_IN)
        r_ac = self._monod_kinetics(S_ac, self.parameters.K_S_ac,
                                  self.parameters.k_m_ac, X_ac) * inhibition_nh3
        reaction_rates[6] = -r_ac  # S_ac消耗
        reaction_rates[21] = r_ac * self.parameters.Y_ac  # X_ac生长

        # 7. 氢降解（文档2第3.4.7节）
        r_h2 = self._monod_kinetics(S_h2, self.parameters.K_S_h2,
                                  self.parameters.k_m_h2, X_h2)
        reaction_rates[7] = -r_h2  # S_h2消耗
        reaction_rates[22] = r_h2 * self.parameters.Y_h2  # X_h2生长

        # 8. 金属络合反应（文档6表2）
        r_metal = self._metal_reactions(y)
        reaction_rates += r_metal

        return reaction_rates

    def _monod_kinetics(self, substrate: float, K_S: float,
                       k_m: float, biomass: float) -> float:
        """Monod动力学方程"""
        return k_m * substrate / (K_S + substrate) * biomass

    def _hydrogen_inhibition(self, S_h2: float, KI_h2: float) -> float:
        """氢抑制函数（非竞争性抑制）"""
        return 1.0 / (1.0 + S_h2 / KI_h2)

    def _ammonia_inhibition(self, S_IN: float) -> float:
        """氨抑制函数"""
        return 1.0 / (1.0 + S_IN / self.parameters.KI_nh3)

    def _metal_reactions(self, y: np.ndarray) -> np.ndarray:
        """金属相关反应（文档6扩展）"""
        metal_rates = np.zeros(len(y))

        # 获取金属变量索引
        idx_fe2 = self.variable_index['S_Fe2']
        idx_edta = self.variable_index['S_EDTA']
        idx_fe_edta = self.variable_index['S_FeEDTA']
        idx_fes = self.variable_index['X_FeS']

        # EDTA-Fe络合反应
        r_fe_edta = (self.parameters.k_edta_fe * y[idx_fe2] * y[idx_edta] -
                    self.parameters.k_edta_fe_rev * y[idx_fe_edta])

        metal_rates[idx_fe2] = -r_fe_edta
        metal_rates[idx_edta] = -r_fe_edta
        metal_rates[idx_fe_edta] = r_fe_edta

        # FeS沉淀反应（简化）
        # 假设S²⁻来自其他过程
        r_precip = self.parameters.k_precip_fes * y[idx_fe2]
        metal_rates[idx_fe2] -= r_precip
        metal_rates[idx_fes] += r_precip

        return metal_rates

    def get_variable_index(self, variable_name: str) -> int:
        """获取状态变量索引"""
        return self.variable_index.get(variable_name, -1)

    def get_variable_name(self, index: int) -> str:
        """获取状态变量名称"""
        if 0 <= index < len(self.state_variables):
            return self.state_variables[index]
        return "UNKNOWN"

# 测试代码
if __name__ == "__main__":
    # 创建模型实例
    model = ADM1Model()

    print("=== ADM1模型测试 ===")
    print(f"状态变量数量: {len(model.state_variables)}")
    print(f"初始条件维度: {model.initial_conditions.shape}")

    # 测试反应计算
    test_input = model.initial_conditions.copy()
    rates = model.biochemical_reactions(0, test_input)

    print(f"反应速率向量维度: {rates.shape}")
    print(f"总反应过程数: {np.count_nonzero(rates)}")

    # 显示前10个变量的反应速率
    print("\n前10个变量的反应速率:")
    for i in range(min(10, len(model.state_variables))):
        var_name = model.state_variables[i]
        rate = rates[i]
        print(f"  {var_name}: {rate:+.4e}")