from book import ContentType

class Model:
    def make_text_prompt(self, text: str, target_language: str) -> str:
        return f"翻译为{target_language}：{text}"

    def make_table_md_prompt(self, table: str, target_language: str) -> str:
        return f"翻译为{target_language}，保持间距（空格，分隔符），以表格形式返回：\n{table}"

    def make_table_txt_prompt(self, table: str, target_language: str) -> str:
        return f"翻译为{target_language}，保持间距（空格，分隔符），以CSV的形式返回：\n{table}"

    def translate_prompt(self, content, target_language: str, file_format: str = 'TXT') -> str:
        if content.content_type == ContentType.TEXT:
            return self.make_text_prompt(content.original, target_language)
        elif content.content_type == ContentType.TABLE:
            if file_format.lower() in ["markdown", "pdf"]:
                return self.make_table_md_prompt(content.get_original_as_str(), target_language)
            elif file_format.lower() == "txt":
                return self.make_table_txt_prompt(content.get_original_as_str(), target_language)

    def make_request(self, prompt):
        raise NotImplementedError("子类必须实现 make_request 方法")
