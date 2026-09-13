# -*- coding: utf-8 -*-
import sys
import io

# ==================== 强制设置输出编码为 UTF-8 ====================
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import pytest
import allure
import logging
import os
from datetime import datetime

# ==================== 日志配置 ====================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "reports", "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")


def log_info(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"{timestamp} - INFO - {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ==================== 测试用例 ====================

@allure.feature("文章接口")
@allure.story("获取单篇文章")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.parametrize("post_id, expected_user_id", [
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
])
def test_get_post_by_id(api_config, http_session, post_id, expected_user_id):
    """测试：根据 ID 获取文章"""
    url = f"{api_config['base_url']}/posts/{post_id}"
    log_info(f"测试获取文章 ID={post_id}")

    response = http_session.get(url, timeout=api_config["timeout"])
    log_info(f"状态码：{response.status_code}")

    assert response.status_code == 200, f"状态码异常：{response.status_code}"

    data = response.json()
    assert data["id"] == post_id, f"文章 ID 不匹配：期望 {post_id}，实际 {data['id']}"
    assert data["userId"] == expected_user_id, f"用户 ID 不匹配：期望 {expected_user_id}，实际 {data['userId']}"
    assert "title" in data, "缺少 title 字段"
    assert "body" in data, "缺少 body 字段"

    log_info(f"[PASS] 文章 ID={post_id} 测试通过！标题：{data['title'][:30]}...")


@allure.feature("文章接口")
@allure.story("获取所有文章")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_get_all_posts(api_config, http_session):
    """测试：获取所有文章"""
    url = f"{api_config['base_url']}/posts"
    log_info("测试获取所有文章")

    response = http_session.get(url, timeout=api_config["timeout"])
    log_info(f"状态码：{response.status_code}")

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list), "返回的不是列表"
    assert len(data) == 100, f"期望 100 篇文章，实际 {len(data)}"

    log_info(f"[PASS] 获取到 {len(data)} 篇文章")


@allure.feature("文章接口")
@allure.story("创建新文章")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
def test_create_post(api_config, http_session, new_post_data):
    """测试：创建新文章"""
    url = f"{api_config['base_url']}/posts"
    log_info("测试创建新文章")

    response = http_session.post(url, json=new_post_data, timeout=api_config["timeout"])
    log_info(f"状态码：{response.status_code}")

    assert response.status_code == 201, f"期望 201，实际 {response.status_code}"

    data = response.json()
    assert data["title"] == new_post_data["title"], "标题不匹配"
    assert data["body"] == new_post_data["body"], "内容不匹配"
    assert data["userId"] == new_post_data["userId"], "用户 ID 不匹配"
    assert "id" in data, "返回数据缺少 id"

    log_info(f"[PASS] 创建成功，新文章 ID={data['id']}")


@allure.feature("文章接口")
@allure.story("更新文章")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_update_post(api_config, http_session):
    """测试：更新文章"""
    url = f"{api_config['base_url']}/posts/1"
    log_info("测试更新文章 ID=1")

    update_data = {
        "id": 1,
        "title": "更新后的标题",
        "body": "更新后的内容",
        "userId": 1
    }

    response = http_session.put(url, json=update_data, timeout=api_config["timeout"])
    log_info(f"状态码：{response.status_code}")

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "更新后的标题", "标题未更新"

    log_info("[PASS] 更新成功")


@allure.feature("文章接口")
@allure.story("删除文章")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_delete_post(api_config, http_session):
    """测试：删除文章"""
    url = f"{api_config['base_url']}/posts/1"
    log_info("测试删除文章 ID=1")

    response = http_session.delete(url, timeout=api_config["timeout"])
    log_info(f"状态码：{response.status_code}")

    assert response.status_code == 200

    log_info("[PASS] 删除成功")


@allure.feature("文章接口")
@allure.story("查询无效文章")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_get_invalid_post(api_config, http_session, invalid_post_id):
    """测试：查询不存在的文章"""
    url = f"{api_config['base_url']}/posts/{invalid_post_id}"
    log_info(f"测试查询无效文章 ID={invalid_post_id}")

    response = http_session.get(url, timeout=api_config["timeout"])
    log_info(f"状态码：{response.status_code}")

    assert response.status_code == 404, f"期望 404，实际 {response.status_code}"

    log_info("[PASS] 无效文章测试通过")


@allure.feature("文章接口")
@allure.story("返回字段完整性")
@allure.severity(allure.severity_level.NORMAL)
def test_post_response_fields(api_config, http_session):
    """测试：检查返回字段完整性"""
    url = f"{api_config['base_url']}/posts/1"
    log_info("测试返回字段完整性")

    response = http_session.get(url, timeout=api_config["timeout"])
    assert response.status_code == 200

    data = response.json()
    required_fields = ["userId", "id", "title", "body"]
    for field in required_fields:
        assert field in data, f"缺少必要字段：{field}"

    log_info("[PASS] 所有必要字段都存在")