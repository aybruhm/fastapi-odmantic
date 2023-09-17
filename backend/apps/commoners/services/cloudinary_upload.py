# Own Imports
from config.secrets import get_settings

# FastAPI Imports
from fastapi import HTTPException

# Third Party Imports
from cloudinary import config
from cloudinary.uploader import upload


class CloudinaryFileUploader:
    """
    This service is responsible for:

    - uploading files to cloudinary.
    """

    def __init__(self) -> None:
        """
        This method is responsible for initializing the uploader object.
        """

        self.settings = get_settings()
        self.config = config(
            api_key=self.settings.CLOUDINARY_API_KEY,
            cloud_name=self.settings.CLOUDINARY_NAME,
            api_secret=self.settings.CLOUDINARY_API_SECRET,
        )

    def upload_file(self, file_path: str) -> None:
        """
        This method uploads a file.

        :param file_path: The path of the audio.
        :type file_path: str
        """

        try:
            data = upload(file=file_path)
            return data["secure_url"]
        except Exception as e:
            raise HTTPException(
                400,
                {
                    "message": "File upload failed",
                    "meta": str(e),
                },
            )


file_uploader = CloudinaryFileUploader()
