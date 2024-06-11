# Yosys Mishandles Bit Operations on Empty Strings

Here is the original Verilog design.

```
module top (y, clk);
  output wire [4:0] y;
  input wire clk; 

  wire [4:0] wire1; 

  assign wire1 = $signed((~""));
  assign y = wire1;
endmodule

```

The original Verilog design appears to treat empty characters as zero during testing with the testbench, resulting in an output of **1**. However, after synthesis with Yosys, the output is instead **0**. The synthesized code is as follows

```

/* Generated by Yosys 0.39+165 (git sha1 22c5ab90d, g++  -fPIC -Os) */

(* src = "rtl.v:1.1-9.10" *)
module top(y, clk);
  (* src = "rtl.v:3.14-3.17" *)
  input clk;
  wire clk;
  (* src = "rtl.v:5.14-5.19" *)
  wire [4:0] wire1;
  (* src = "rtl.v:2.21-2.22" *)
  output [4:0] y;
  wire [4:0] y;
  assign wire1 = 5'h00;
  assign y = 5'h00;
endmodule

```

![97e649ca754528f0b26e79d4cd4abb79](./Inconsistent.png)
