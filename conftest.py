import pytest
import requests
import os
import yaml
from dotenv import load_dotenv

# ==================== 获取项目根目录 ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==================== 加载环境变量 ====================
load_dotenv(os.path.join(BASE_DIR, ".env"))

# ==================== 加载配置文件 ====================
with open(os.path.join(BASE_DIR, "config.yaml"), "r", encoding="utf-8") as f:
    CONFIG = yaml.safe_load(f)

# ==================== 加载测试数据 ====================
with open(os.path.join(BASE_DIR, "data.yaml"), "r", encoding="utf-8") as f:
    DATA = yaml.safe_load(f)


# ==================== 注册自定义标记 ====================
def pytest_configure(config):
    config.addinivalue_line("markers", "smoke: 冒烟测试")
    config.addinivalue_line("markers", "regression: 回归测试")


# ==================== 全局 Fixture ====================

@pytest.fixture(scope="session")
def api_config():
    """API 配置（整个会话只读取一次）"""
    return {
        "base_url": os.getenv("BASE_URL", CONFIG["api"]["base_url"]),
        "timeout": CONFIG["api"]["timeout"]
    }


@pytest.fixture(scope="function")
def http_session():
    """每个测试创建一个新的 Session"""
    session = requests.Session()
    session.headers.update({"User-Agent": "pytest-test"})
    yield session
    session.close()


@pytest.fixture
def all_posts():
    """所有测试文章数据"""
    return DATA["test_posts"]


@pytest.fixture
def new_post_data():
    """新文章数据"""
    return DATA["new_post"]


@pytest.fixture
def invalid_post_id():
    """无效的文章 ID"""
    return CONFIG["test"]["invalid_post_id"]