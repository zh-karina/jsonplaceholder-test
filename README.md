 JSONPlaceholder 接口自动化测试框架 📝

基于 **Pytest + Requests + Allure + Jenkins** 的接口自动化测试框架

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Pytest](https://img.shields.io/badge/Pytest-9.1.1-green)
![Allure](https://img.shields.io/badge/Allure-2.27.0-orange)
![Jenkins](https://img.shields.io/badge/Jenkins-2.568.3-red)

---

## 📖 项目介绍

本项目是一个完整的 RESTful API 自动化测试框架，基于 JSONPlaceholder 实现。覆盖 **GET / POST / PUT / DELETE** 四种请求方式，包括**正向测试、异常测试、字段完整性测试**等场景，集成 **Allure 报告** 和 **Jenkins 持续集成**。

---

## 🛠️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Python | 3.10 | 编程语言 |
| Pytest | 9.1.1 | 测试框架 |
| Requests | 2.31.0 | HTTP 客户端 |
| PyYAML | 6.0.1 | 数据驱动 |
| Allure | 2.27.0 | 测试报告 |
| Jenkins | 2.568.3 | 持续集成 |
| pytest-html | 4.1.1 | HTML 报告 |

---

## 📁 项目结构
jsonplaceholder-test/
├── .env # 环境变量
├── config.yaml # 配置文件
├── data.yaml # 测试数据
├── conftest.py # Pytest 共享配置
├── test_posts.py # 测试用例
├── send_email.py # 邮件发送脚本
├── requirements.txt # 依赖清单
└── reports/ # 测试报告目录
├── html/
├── logs/
└── allure-results/

text

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/zh-karina/jsonplaceholder-test.git
cd jsonplaceholder-test
2. 安装依赖
bash
pip install -r requirements.txt
3. 运行测试
bash
# 基础运行
pytest test_posts.py -v

# 生成 Allure 报告
pytest test_posts.py -v --alluredir=reports/allure-results
allure serve reports/allure-results
🧪 测试用例
编号	用例名称	方法	说明
1	test_get_post_by_id	GET	根据 ID 获取文章（参数化 5 个 ID）
2	test_get_all_posts	GET	获取所有文章（100 篇）
3	test_create_post	POST	创建新文章，验证 201
4	test_update_post	PUT	更新文章
5	test_delete_post	DELETE	删除文章
6	test_get_invalid_post	GET	查询不存在的文章，验证 404
7	test_post_response_fields	GET	返回字段完整性校验
📊 测试报告
Allure 报告：可视化展示、分类统计

HTML 报告：轻量级、自动生成

🔄 持续集成
定时执行：每天凌晨自动运行

邮件通知：构建完成后自动发送测试报告

📈 项目亮点
✅ RESTful 全方法覆盖：GET / POST / PUT / DELETE

✅ 参数化测试：数据驱动，一处修改多处生效

✅ 异常场景：无效 ID、字段缺失等

✅ 持续集成：Jenkins 定时执行 + 邮件通知

✅ 报告可视化：Allure + HTML 双报告

📝 作者
zh-karina

GitHub: @zh-karina
