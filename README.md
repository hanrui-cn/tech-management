# 技术管理书籍

这是一本关于技术管理的书籍，旨在分享在技术管理领域的经验和见解。

## 项目结构

- `src/` - LaTeX 源文件目录
- `build/` - 编译输出目录
- `Makefile` - 构建脚本

## 构建说明

要构建 PDF 文件，请运行：

```bash
make build
```

生成的 PDF 将位于 `build/main.pdf`。

## 清理

要清理生成的文件，请运行：

```bash
make clean
```