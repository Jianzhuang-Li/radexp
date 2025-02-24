## Sketchup建筑建模

1. 围护结构

2. 导出radfiles	

## Radiance环境渲染

1. 在wsl环境中生成"oct"文件, windows环境中会生成的oct文件不可用

	```
	oconv  -f 5zoneAuto.rad materials.rad  skies/Site_1_1108_1219.sky > scene.oct
	```

2. 使用rvu指令查看oct环境文件(在windows下)

	```
	rvu -vf .\views\5zoneAuto.vf  -w -av .60 .60 .60 -R .\5zoneAuto.rif -ab 5 -ad 230 scene.oct
	```

## 获取三相法视图矩阵

1. 将原来的玻璃材质替换为发光源, 并确认光源的法线方向向内

	```
	# 注意窗户的法向量朝内(坐标按右手螺旋方向自上而下排列)
	# 不同方向的窗户组成一组窗户，然后使用同一种发光材质(内容相同，但是命名不同)
	# 是为了区分开，方便后面创建视图矩阵和日光矩阵
	void glow windowglow_east
	0
	0
	4 1 1 1 0

	windowglow polygon window
	0
	0
	12  0.5 -1.5 1
		0.5 -1.5 2
		3.5 -1.5 2
		3.5 -1.5 1
	```

2. 创建传感器位置及法向量文件
	
	```
	# 按行排列， 前三个是坐标, 后三个是法向量, 一般用(0, 0, 1), 文件命名为5zoneAuto.pts
	nx ny nz ux uy uz
	```

3. 创建光传感器视图矩阵

	```
	# "OpenStudio_Window_Ext_xx"是步骤1中创建的发光材质
	# klems_int缺失, 可以使用klems_full
	rcontrib -f klems_int.cal -bn Nkbins -fo -o results/photocells_%s.vmx \
	 -b kbinS -m OpenStudio_Window_Ext_south \
	 -b kbinE -m OpenStudio_Window_Ext_east \
	 -b kbinW -m OpenStudio_Window_Ext_west \
	 -b kbinN -m OpenStudio_Window_Ext_north \
	 -I+ -ab 2 -ad 50000 -lw 2e-5 scene.oct < view/5zoneAuto.pts 
	```
4. 每组窗户创建一个单独的rad文件

	```
	## clear_glass_4
	void glass clear_glass_4
	0
	0
	3 1 1 1

	void alias OpenStudio_Window_Ext clear_glass_4
	# east window
	OpenStudio_Window_Ext polygon t_2_0
	0
	0
	12
    30.500000  11.400000  2.100000
    30.500000  11.400000  0.900000
    30.500000  3.800000  0.900000
    30.500000  3.800000  2.100000
	```

5. 创建日光矩阵

	```
	# vd 是窗户的外法线方向， sky是天空材质
	genklemsamp -vd 0 -1 0 windows/5zoneAuto_south.rad | \
		rcontrib -c 1000 -e MF:4 -f reinhart.cal -b rbin -bn Nrbins -m sky_glow \
		-faf scene_dmx.oct > results/south.dmx
	```

6. 计算传感器点的照度

	```
	rlam '!dctimestep results/photocells_Openstudio_Window_Ext_east.vmx xml/type25_anglenull.xml results/east.dmx skv/6_30_10.skv' \
		'!dctimestep results/photocells_Openstudio_Window_Ext_west.vmx xml/type25_anglenull.xml results/west.dmx skv/6_30_10.skv' \
		'!dctimestep results/photocells_Openstudio_Window_Ext_south.vmx xml/type25_anglenull.xml results/south.dmx skv/6_30_10.skv' \
		'!dctimestep results/photocells_Openstudio_Window_Ext_north.vmx xml/type25_anglenull.xml results/north.dmx skv/6_30_10.skv' | \
		rcalc -e '$1=179*($1+$4+$7+$10)*0.25+($2+$5+$8+$11)*0.670+($3+$6+$9+$12)*0.065 > results/illu_0630.dat
	```