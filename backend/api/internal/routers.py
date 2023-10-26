from fastapi import HTTPException, Query, APIRouter
from starlette.responses import FileResponse
import os
from config.settings import settings

current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

router = APIRouter(tags=["Chat bot"], prefix="/api/internal")


@router.get("/api/download")
def download_file(user_id: str = Query(...), filename: str = Query(...)):
    save_dir = os.path.join(current_dir, settings.common.UPLOAD_FOLDER, user_id)
    file_path = os.path.join(save_dir, filename)

    if os.path.exists(file_path):
        return FileResponse(file_path, headers={"Content-Disposition": f"attachment; filename={filename}"})
    else:
        raise HTTPException(status_code=404, detail="File not found")
