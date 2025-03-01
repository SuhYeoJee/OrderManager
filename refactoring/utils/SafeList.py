class SafeList(list):
    def safe_get(self, index, default=None):
        """인덱스 오류 회피"""
        return self[index] if 0 <= index < len(self) else default