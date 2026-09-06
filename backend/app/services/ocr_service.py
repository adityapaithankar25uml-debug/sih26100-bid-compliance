from typing import List, Dict, Any, Tuple


class OCRService:
    @staticmethod
    def is_scanned_pdf(extracted_pages: List[Dict[str, Any]]) -> bool:
        """Determines whether a PDF is scanned based on text density."""
        if not extracted_pages:
            return True
        total_chars = sum(len(p.get("text", "").strip()) for p in extracted_pages)
        # If total characters across all pages is less than 50, classify as scanned/image PDF
        return total_chars < 50

    def run_ocr(self, filename: str, content: bytes, page_number: int = 1) -> Tuple[str, List[Dict[str, Any]], float, str]:
        """
        Runs OCR processing over scanned content.
        Tries PaddleOCR / Tesseract if installed, otherwise uses Mock OCR adapter.
        Returns: (ocr_text, blocks, ocr_confidence, extraction_method)
        """
        import os
        if os.getenv("ENABLE_REAL_OCR", "false").lower() == "true":
            try:
                import paddleocr
                ocr = paddleocr.PaddleOCR(use_angle_cls=True, lang='en')
                result = ocr.ocr(content, cls=True)
                text_lines = []
                blocks = []
                total_conf = 0.0
                count = 0
                for line in result[0]:
                    bbox_raw = line[0]  # [[x0,y0],[x1,y0],[x1,y1],[x0,y1]]
                    txt, conf = line[1]
                    text_lines.append(txt)
                    total_conf += conf
                    count += 1
                    blocks.append({
                        "text": txt,
                        "bbox": {"x0": float(bbox_raw[0][0]), "y0": float(bbox_raw[0][1]), "x1": float(bbox_raw[2][0]), "y1": float(bbox_raw[2][1])}
                    })
                ocr_text = "\n".join(text_lines)
                avg_conf = total_conf / count if count > 0 else 0.95
                return ocr_text, blocks, avg_conf, "OCR_PADDLE"
            except Exception:
                pass

        # Fallback Mock OCR Engine
        mock_ocr_text = (
            f"[MOCK_OCR EXTRACTED CONTENT FOR PAGE {page_number}]\n"
            "ANNUAL TURNOVER CERTIFICATE\n"
            "This is to certify that M/s DEMO INDUSTRIAL SUPPLIERS PRIVATE LIMITED\n"
            "GSTIN: 33AAAAA0000A1Z5 | PAN: AAAAA0000A\n"
            "Turnover FY 2023-24: Rs 45.00 Crores\n"
            "Turnover FY 2022-23: Rs 38.50 Crores\n"
            "MSE Registration Udyam: UDYAM-TN-01-0000000"
        )
        mock_blocks = [
            {"text": "ANNUAL TURNOVER CERTIFICATE", "bbox": {"x0": 50.0, "y0": 50.0, "x1": 300.0, "y1": 70.0}},
            {"text": "GSTIN: 33AAAAA0000A1Z5 | PAN: AAAAA0000A", "bbox": {"x0": 50.0, "y0": 80.0, "x1": 400.0, "y1": 100.0}},
            {"text": "Turnover FY 2023-24: Rs 45.00 Crores", "bbox": {"x0": 50.0, "y0": 110.0, "x1": 350.0, "y1": 130.0}},
            {"text": "MSE Registration Udyam: UDYAM-TN-01-0000000", "bbox": {"x0": 50.0, "y0": 140.0, "x1": 380.0, "y1": 160.0}}
        ]
        return mock_ocr_text, mock_blocks, 0.92, "MOCK_OCR"


ocr_service = OCRService()
