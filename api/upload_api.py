"""
文件上传 API (FastAPI 版本)
支持上传 .sql, .doc, .docx, .pdf, .xls, .xlsx 文件
"""
import os
import sys
from datetime import datetime, date
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from werkzeug.utils import secure_filename

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# 创建路由器
router = APIRouter(prefix="/api", tags=["上传"])

# 允许的文件扩展名
ALLOWED_EXTENSIONS = {
    'sql': ['.sql'],
    'document': ['.doc', '.docx', '.pdf', '.xls', '.xlsx', '.txt', '.csv']
}


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    train_type: Optional[str] = Form(None)
):
    """文件上传接口"""
    try:
        original_filename = file.filename
        
        # 判断文件类型
        ext = Path(original_filename).suffix.lower()
        
        if ext in ALLOWED_EXTENSIONS['sql']:
            file_type = 'sql'
        elif ext in ALLOWED_EXTENSIONS['document']:
            file_type = 'document'
        else:
            raise HTTPException(
                status_code=400,
                detail="不支持的文件类型，请上传 .sql, .doc, .docx, .pdf, .xls, .xlsx 格式的文件"
            )
        
        # 可以通过参数强制指定类型
        if train_type and train_type in ['sql', 'document']:
            file_type = train_type
        
        # 获取上传路径
        today = datetime.now().strftime('%Y-%m-%d')
        if file_type == 'sql':
            base_path = PROJECT_ROOT / 'train-sql' / today
        else:
            base_path = PROJECT_ROOT / 'train-document' / today
        
        base_path.mkdir(parents=True, exist_ok=True)
        
        # 生成安全的文件名
        timestamp = datetime.now().strftime('%H%M%S')
        filename = secure_filename(original_filename)
        name, file_ext = os.path.splitext(filename)
        
        if not name:
            name = f"file_{timestamp}"
        
        final_filename = f"{name}_{timestamp}{file_ext}"
        file_path = base_path / final_filename
        
        # 保存文件
        content = await file.read()
        with open(file_path, 'wb') as f:
            f.write(content)
        
        print(f"[Upload] 文件已保存: {file_path}")
        
        # 计算相对路径和文件信息
        relative_path = file_path.relative_to(PROJECT_ROOT)
        file_size = file_path.stat().st_size
        file_ext_clean = file_ext.lstrip('.').lower() if file_ext else 'unknown'
        
        # 插入数据库记录
        try:
            from api.data_manage_api import insert_training_file, calculate_file_hash
            file_hash = calculate_file_hash(file_path)
            record_id = insert_training_file(
                file_name=final_filename,
                file_path=str(relative_path),
                file_type=file_ext_clean,
                train_type=file_type,
                file_size=file_size,
                file_hash=file_hash,
                upload_date=date.today()
            )
            print(f"[Upload] 数据库记录已插入, ID: {record_id}")
        except Exception as db_err:
            import traceback
            print(f"[Upload] 插入数据库记录失败: {db_err}")
            print(traceback.format_exc())
        
        return {
            "success": True,
            "message": "上传成功，请点击对应的训练按钮开始训练",
            "file_name": final_filename,
            "file_path": str(relative_path),
            "train_type": file_type,
            "file_size": file_size
        }
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"[Upload] 上传失败: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"上传失败: {str(e)}")
