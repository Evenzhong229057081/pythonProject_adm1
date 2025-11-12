# src/interface/parameter_table.py
"""
ADM1参数表格界面 - 修复categories变量引用错误
"""

import sys
from pathlib import Path


class ParameterTable:
    """参数表格显示器 - 修复版"""

    def __init__(self):
        self.setup = False
        self.model = None
        self.param_manager = None

    def _print_status(self, message, status='info'):
        """打印状态消息"""
        prefixes = {
            'success': '[SUCCESS]',
            'error': '[ERROR]',
            'warning': '[WARNING]',
            'info': '[INFO]'
        }
        prefix = prefixes.get(status, '[INFO]')
        print(f"{prefix} {message}")

    def initialize(self):
        """初始化组件"""
        try:
            src_path = Path(__file__).parent.parent
            if str(src_path) not in sys.path:
                sys.path.insert(0, str(src_path))

            from patches.environment_patch import safe_import

            base_path = Path(__file__).parent.parent

            ADM1Model = safe_import(base_path / 'core/adm1_model.py', 'ADM1Model')
            ADM1ParameterManager = safe_import(base_path / 'parameters/parameter_manager.py', 'ADM1ParameterManager')

            if ADM1Model and ADM1ParameterManager:
                self.model = ADM1Model()
                self.param_manager = ADM1ParameterManager()
                self.setup = True
                self._print_status("组件初始化成功", 'success')
                return True
            else:
                self._print_status("模块导入失败", 'error')
                return False

        except Exception as e:
            self._print_status(f"初始化失败: {e}", 'error')
            return False

    def get_parameter_data(self, preset_name="food_waste"):
        """获取参数数据"""
        if not self.setup or not self.param_manager:
            return None

        try:
            self.param_manager.set_current_preset(preset_name)
            return self.param_manager.get_current_parameters()
        except Exception as e:
            self._print_status(f"获取参数数据失败: {e}", 'error')
            return None

    def display_comprehensive_table(self, preset_name="food_waste"):
        """显示综合参数表格"""
        print("=" * 80)
        print(f"ADM1模型参数详细表格 - {preset_name}")
        print("=" * 80)

        if not self.initialize():
            return

        param_data = self.get_parameter_data(preset_name)
        if not param_data:
            self._print_status("无法获取参数数据", 'error')
            return

        if param_data.get('description'):
            print(f"预设描述: {param_data['description']}")

        # 显示各参数组
        self._display_kinetic_parameters(param_data.get('kinetic_parameters', {}))
        self._display_initial_concentrations(param_data.get('initial_conditions', {}))
        self._display_other_parameters(param_data)

        print("=" * 80)
        self._print_status("参数表格显示完成", 'success')

    def _display_kinetic_parameters(self, kinetic_params):
        """显示动力学参数 - 修复categories错误"""
        if not kinetic_params:
            self._print_status("无动力学参数数据", 'warning')
            return

        print("\n" + "-" * 60)
        print("动力学参数 (k-values)")
        print("-" * 60)

        # 修复：先定义所有已知类别，再计算其他参数
        known_categories = {
            '水解速率常数': ['k_hyd_ch', 'k_hyd_pr', 'k_hyd_li'],
            '最大摄取速率': ['k_m_su', 'k_m_aa', 'k_m_fa', 'k_m_c4', 'k_m_pro', 'k_m_ac', 'k_m_h2'],
            '半饱和常数': ['K_S_su', 'K_S_aa', 'K_S_fa', 'K_S_c4', 'K_S_pro', 'K_S_ac', 'K_S_h2'],
            '抑制常数': ['K_I_h2'],
            '产率系数': ['Y_su', 'Y_aa', 'Y_fa', 'Y_c4', 'Y_pro', 'Y_ac', 'Y_h2']
        }

        # 计算其他参数（不包括k_dis）
        all_known_params = [param for category in known_categories.values() for param in category]
        other_params = [k for k in kinetic_params.keys() if k not in all_known_params and k != 'k_dis']

        # 合并categories
        categories = known_categories.copy()
        if other_params:
            categories['其他动力学参数'] = other_params

        # 先显示k_dis
        if 'k_dis' in kinetic_params:
            description = self._get_parameter_description('k_dis')
            print(f"k_dis: {kinetic_params['k_dis']:.6e}  {description}")
            print()

        # 显示其他参数
        for category, params in categories.items():
            displayed_params = [p for p in params if p in kinetic_params]
            if displayed_params:
                print(f"{category}:")
                for param in displayed_params:
                    description = self._get_parameter_description(param)
                    print(f"  {param:12} {kinetic_params[param]:12.6e}  {description}")
                print()

    def _display_initial_concentrations(self, concentrations):
        """显示初始浓度"""
        if not concentrations:
            self._print_status("无初始浓度数据", 'warning')
            return

        print("\n" + "-" * 60)
        print("物质初始浓度")
        print("-" * 60)

        # 分类显示
        categories = {
            '可溶性底物': [var for var in concentrations.keys() if
                           var.startswith('S_') and var not in ['S_cat', 'S_an']],
            '颗粒性物质': [var for var in concentrations.keys() if var.startswith('X_')],
            '离子物质': [var for var in concentrations.keys() if var in ['S_cat', 'S_an']]
        }

        for category, variables in categories.items():
            displayed_vars = [var for var in variables if var in concentrations]
            if displayed_vars:
                print(f"{category}:")
                for var in displayed_vars:
                    description = self._get_variable_description(var)
                    print(f"  {var:8} {concentrations[var]:12.6e}  {description}")
                print()

    def _display_other_parameters(self, param_data):
        """显示其他参数组"""
        # 金属参数
        metal_params = param_data.get('metal_parameters', {})
        if metal_params:
            print("\n" + "-" * 60)
            print("金属相关参数")
            print("-" * 60)
            for param, value in metal_params.items():
                description = self._get_parameter_description(param)
                print(f"{param:15} {value:12.6e}  {description}")

        # 物理参数
        physical_params = param_data.get('physical_parameters', {})
        if physical_params:
            print("\n" + "-" * 60)
            print("物理化学参数")
            print("-" * 60)
            for param, value in physical_params.items():
                description = self._get_parameter_description(param)
                print(f"{param:15} {value:12.6e}  {description}")

    def _get_parameter_description(self, param_name):
        """获取参数描述"""
        descriptions = {
            'k_dis': 'disintegration rate constant',
            'k_hyd_ch': 'carbohydrate hydrolysis rate constant',
            'k_hyd_pr': 'protein hydrolysis rate constant',
            'k_hyd_li': 'lipid hydrolysis rate constant',
            'k_m_su': 'maximum uptake rate for sugars',
            'k_m_aa': 'maximum uptake rate for amino acids',
            'k_m_fa': 'maximum uptake rate for LCFA',
            'k_m_c4': 'maximum uptake rate for C4+',
            'k_m_pro': 'maximum uptake rate for propionate',
            'k_m_ac': 'maximum uptake rate for acetate',
            'k_m_h2': 'maximum uptake rate for hydrogen',
            'K_S_su': 'half-saturation constant for sugars',
            'K_S_aa': 'half-saturation constant for amino acids',
            'K_S_fa': 'half-saturation constant for LCFA',
            'K_S_c4': 'half-saturation constant for C4+',
            'K_S_pro': 'half-saturation constant for propionate',
            'K_S_ac': 'half-saturation constant for acetate',
            'K_S_h2': 'half-saturation constant for hydrogen',
            'K_I_h2': 'hydrogen inhibition constant',
            'Y_su': 'yield coefficient for sugars',
            'Y_aa': 'yield coefficient for amino acids',
            'Y_fa': 'yield coefficient for LCFA',
            'Y_c4': 'yield coefficient for C4+',
            'Y_pro': 'yield coefficient for propionate',
            'Y_ac': 'yield coefficient for acetate',
            'Y_h2': 'yield coefficient for hydrogen',
            'k_dec': 'decay rate constant',
            'k_edta_fe': 'EDTA-Fe complexation rate constant',
            'k_precip_fes': 'FeS precipitation rate constant',
            'KI_Fe': 'iron inhibition constant',
            'KI_Ni': 'nickel inhibition constant',
            'KI_Co': 'cobalt inhibition constant',
            'kLa': 'liquid-gas transfer coefficient',
            'K_H_co2': 'CO2 Henry constant',
            'K_H_ch4': 'CH4 Henry constant',
            'K_H_h2': 'H2 Henry constant'
        }
        return descriptions.get(param_name, '')

    def _get_variable_description(self, var_name):
        """获取变量描述"""
        descriptions = {
            'S_su': 'monosaccharides',
            'S_aa': 'amino acids',
            'S_fa': 'long chain fatty acids',
            'S_va': 'valerate',
            'S_bu': 'butyrate',
            'S_pro': 'propionate',
            'S_ac': 'acetate',
            'S_h2': 'hydrogen',
            'S_ch4': 'methane',
            'S_ic': 'inorganic carbon',
            'S_in': 'inorganic nitrogen',
            'S_I': 'soluble inerts',
            'X_c': 'composites',
            'X_ch': 'carbohydrates',
            'X_pr': 'proteins',
            'X_li': 'lipids',
            'X_su': 'sugar degraders',
            'X_aa': 'amino acid degraders',
            'X_fa': 'LCFA degraders',
            'X_c4': 'C4+ degraders',
            'X_pro': 'propionate degraders',
            'X_ac': 'acetate degraders',
            'X_h2': 'hydrogen degraders',
            'X_I': 'particulate inerts',
            'S_cat': 'cations',
            'S_an': 'anions'
        }
        return descriptions.get(var_name, '')


def main():
    """主函数"""
    table = ParameterTable()
    table.display_comprehensive_table()


if __name__ == "__main__":
    main()