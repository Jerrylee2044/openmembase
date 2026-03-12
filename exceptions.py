"""
OpenMemBase 异常定义 - 企业级错误处理
"""


class OpenMemBaseError(Exception):
    """OpenMemBase 基础异常"""
    
    def __init__(self, message: str, code: str = "UNKNOWN", details: dict = None):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> dict:
        return {
            "error": True,
            "code": self.code,
            "message": self.message,
            "details": self.details
        }


class ConfigurationError(OpenMemBaseError):
    """配置错误"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "CONFIG_ERROR", details)


class DatabaseError(OpenMemBaseError):
    """数据库错误"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "DB_ERROR", details)


class EmbeddingError(OpenMemBaseError):
    """Embedding 错误"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "EMBEDDING_ERROR", details)


class SearchError(OpenMemBaseError):
    """搜索错误"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "SEARCH_ERROR", details)


class ProjectError(OpenMemBaseError):
    """项目错误"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "PROJECT_ERROR", details)


class ResourceError(OpenMemBaseError):
    """资源错误"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "RESOURCE_ERROR", details)


class ValidationError(OpenMemBaseError):
    """验证错误"""
    
    def __init__(self, message: str, field: str = None, details: dict = None):
        d = details or {}
        if field:
            d["field"] = field
        super().__init__(message, "VALIDATION_ERROR", d)


class NotFoundError(OpenMemBaseError):
    """未找到错误"""
    
    def __init__(self, resource_type: str, identifier: str):
        super().__init__(
            f"{resource_type} 未找到: {identifier}",
            "NOT_FOUND",
            {"resource_type": resource_type, "id": identifier}
        )


class PermissionError(OpenMemBaseError):
    """权限错误"""
    
    def __init__(self, message: str = "权限不足"):
        super().__init__(message, "PERMISSION_DENIED")


class RateLimitError(OpenMemBaseError):
    """速率限制错误"""
    
    def __init__(self, message: str = "请求过于频繁", retry_after: int = 60):
        super().__init__(message, "RATE_LIMIT", {"retry_after": retry_after})


class ArchiveError(OpenMemBaseError):
    """归档错误"""
    
    def __init__(self, message: str, details: dict = None):
        super().__init__(message, "ARCHIVE_ERROR", details)


# 错误代码映射
ERROR_CODES = {
    "CONFIG_ERROR": 400,
    "DB_ERROR": 500,
    "EMBEDDING_ERROR": 503,
    "SEARCH_ERROR": 500,
    "PROJECT_ERROR": 400,
    "RESOURCE_ERROR": 400,
    "VALIDATION_ERROR": 422,
    "NOT_FOUND": 404,
    "PERMISSION_DENIED": 403,
    "RATE_LIMIT": 429,
    "ARCHIVE_ERROR": 500,
    "UNKNOWN": 500
}


def get_http_status(code: str) -> int:
    """获取 HTTP 状态码"""
    return ERROR_CODES.get(code, 500)
