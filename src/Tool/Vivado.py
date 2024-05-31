import os
import subprocess


class Vivado:
    def __init__(self, vivado_bin=None, vivado_desc="vivado", vivado_output="syn_vivado.v"):
        self.vivado_bin = vivado_bin
        self.vivado_desc = vivado_desc
        self.vivado_output = vivado_output

    def __str__(self):
        return self.vivado_desc

    # def run_synth(self, top, v_file, output_dir):  # 添加 output_dir 参数，默认为当前目录
    #     vivado_tcl = os.path.join(output_dir, f"vivado_{top}.tcl")  # 更新TCL脚本路径
    #
    #
    #     with open(vivado_tcl, 'w') as f:
    #         f.write(self.vivado_synthesis_config(top))  # 更新输出路径
    #
    #     subprocess.run(["sed", "s/^module/(* use_dsp48=\"no\" *) (* use_dsp=\"no\" *) module/;", "-i", v_file])
    #     vivado_bin = self.vivado_bin if self.vivado_bin else "vivado"
    #
    #     # 改变当前工作目录
    #     os.chdir(output_dir)
    #     vivado_tcl = f"vivado_{top}.tcl"
    #
    #
    #     result = subprocess.run([vivado_bin, "-mode", "batch", "-source", vivado_tcl], capture_output=True, text=True)
    #     if result.returncode != 0:
    #         print("Synthesis failed:", result.stderr)
    #     else:
    #         print("Synthesis succeeded")
    def run_synth(self, top, v_file, output_dir):  # 添加 output_dir 参数，默认为当前目录
        vivado_tcl = os.path.join(output_dir, f"vivado_{top}.tcl")  # 更新TCL脚本路径

        with open(vivado_tcl, 'w') as f:
            f.write(self.vivado_synthesis_config(top))  # 更新输出路径

        subprocess.run(["sed", "s/^module/(* use_dsp48=\"no\" *) (* use_dsp=\"no\" *) module/;", "-i", v_file])
        vivado_bin = self.vivado_bin if self.vivado_bin else "vivado"

        # 改变当前工作目录
        os.chdir(output_dir)
        vivado_tcl = f"vivado_{top}.tcl"

        try:
            result = subprocess.run([vivado_bin, "-mode", "batch", "-source", vivado_tcl], capture_output=True,
                                    text=True)
            result.check_returncode()  # This will raise an exception if returncode is non-zero
        except subprocess.CalledProcessError as e:
            print("### Vivado Synthesis Error ###\n\n", e.stderr)
            raise  # Re-raise the exception

        print("### Vivado Synthesis Success ###\n")
        print("### Finished synthesis with Vivado ###\n")


    def vivado_synthesis_config(self, top):
        config_lines = [
            "# CRITICAL WARNING: [Synth 8-5821] Potential divide by zero",
            "set_msg_config -id {Synth 8-5821} -new_severity {WARNING}",
            "",
            f"read_verilog rtl.v",
            f"synth_design -part xc7k70t -top {top}",
            f"write_verilog -force syn_vivado.v"
        ]
        return "\n".join(config_lines)

# 使用示例
# vivado = Vivado()
# vivado.run_synth("top", "rtl.v", output_dir="output_directory")
