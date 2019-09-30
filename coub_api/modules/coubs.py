""".. module:: coubs

    This module provide and API, using it you can obtain coub's metadata, edit its properties or delete the coub.

    Also this module provide api for creating COUB.
    
"""

from typing import Dict, List

from coub_api.modules.base import TmpBaseConnector, connector_return_type
from coub_api.schemas.coub import BigCoub
from coub_api.schemas.constants import VisibilityType

__all__ = ("Coubs",)


class Coubs(TmpBaseConnector):
    """
    Class for
    :mod: `get_coub`,  :mod: `edit_coub`, :mod: `delete_coub`, :mod: `init_upload`,
    :mod: `upload_video`, :mod: `upload_audio`, :mod: `finalize_upload` interface
    """

    __slots__ = ()

    def _get_coub_response(self, coub_id: str) -> connector_return_type:
        url = self.build_url(f"/coubs/{coub_id}")
        return self.request("get", url)

    def get_coub(self, coub_id: str) -> BigCoub:
        """
        Getting coub data

        Resource endpoint:
            GET /api/v2/coubs/:id
        
        >>> api = CoubApi()
        >>> coub = api.coubs.get_coub("1jf5v1")
        >>> print(coub.id)
        "1jf5v1"

        :param coub_id: int the identifier of the required coub
        :return: BigCoub pydantic schema
        """
        return BigCoub(**self._get_coub_response(coub_id).json())

    def _edit_coub_response(
        self,
        coub_permalink: str,
        channel_id: int,
        *,
        title: str,
        tags: List[str],
        visibility_type: VisibilityType,
    ) -> connector_return_type:
        url = self.build_url(f"/coubs/{coub_permalink}/update_info")
        params = {
            "coub[channel_id]": channel_id,
            "coub[title]": title,
            "coub[tags]": ",".join(tags),
            "coub[original_visibility_type]": visibility_type,
        }
        return self.authenticated_request("post", url, params=params)

    def edit_coub(
        self,
        coub_permalink: str,
        channel_id: int,
        *,
        title: str,
        tags: List[str],
        visibility_type: VisibilityType = VisibilityType.PRIVATE,
    ) -> BigCoub:
        """
        Editing coub data.
    
        Resource endpoint:
            POST /api/v2/coubs/:id/update_info

        :param coub_permalink: the identifier of the required coub
        :param channel_id: new id of the channel
        :param title: new title of the coub
        :param tags: new tags assigned to the coub
        :param visibility_type: enum of the :mod: VisibilityType
        :return: BigCoub pydantic schema
        """
        data = self._edit_coub_response(
            coub_permalink,
            channel_id,
            title=title,
            tags=tags,
            visibility_type=visibility_type,
        )
        return BigCoub(**data.json())

    def delete_coub(self, coub_permalink: str):
        """
        .. note:: Not working now, help required.
        
        :param coub_permalink: the identifier of the required coub
        :return:
        """
        raise NotImplementedError

    def init_upload(self) -> Dict[str, str]:
        """
        A coub consists of two parts: the video sample and the audio track.

        To create a coub via API you need to:
            #. Initialize the upload and get the id for the upload;
            #. Add a video for the coub;
            #. Add an audio track for the coub;
            #. Finalize the coub.
        
        Find more at https://coub.com/dev/docs/Coub+API%2FCreating+coub
    
        Resource endpoint:
            POST /api/v2/coubs/init_upload
    
        Small sample for start uploading.

        >>> from coub_api import CoubApi
        >>> import os
        >>> access_token = os.environ.get("coub_access_token")
        >>> api = CoubApi()
        >>> api.authenticate(access_token)
        >>> coub = api.coubs.get_coub("1jf5v1")
        {"permalink":"1jik0b","id":93927327}

        :return: permalink and id for new Coub
        """
        url = self.build_url("/coubs/init_upload")
        return self.authenticated_request("post", url).json()

    def upload_video(
        self, coub_id: int, video_path: str, content_type: str = "video/mp4"
    ) -> Dict[str, str]:
        """
        Add a video for the coub.

        Resource endpoint:
            POST /api/v2/coubs/:id/upload_video
        
        :param coub_id: id from :mod: init_upload step
        :param video_path: path to video on your filesystem (PosixPath('/home/devel/video.mp4'))
        :param content_type: choosen content_type for video file. Find more types at https://gist.github.com/Derfirm/5b11f77d64816153024e979141b69800
        :return: {"status": "ok"} if if the request successed; {"message": "error"} otherwise

        Upload video-file from filesystem.
        
        >>> api.coubs.upload_video(93927327, "video.mp4")
        {"status": "ok"}
        """
        url = self.build_url(f"/coubs/{coub_id}/upload_video")
        headers = {"Content-type": content_type}
        return self.authenticated_request(
            "post", url, data=open(video_path, "rb"), headers=headers
        ).json()

    def upload_audio(
        self, coub_id: int, audio_path: str, content_type: str = "audio/mpeg"
    ) -> Dict[str, str]:
        """
        Add an audio for the coub.

        Resource endpoint:
            POST /api/v2/coubs/:id/upload_video

        :param coub_id: id from :mod: init_upload step
        :param audio_path: path to video on your filesystem (PosixPath('/home/devel/audio.mp4'))
        :param content_type: choosen content_type for audio file. Find more types at https://gist.github.com/Derfirm/5b11f77d64816153024e979141b69800
        :return: {"status": "ok"} if if the request successed; {"message": "error"} otherwise
        
        Upload audio-file from filesystem.
        
        >>> api.coubs.upload_video(93927327, "audio.mp3")
        {"status": "ok"}

        """
        headers = {"Content-type": content_type}
        url = self.build_url(f"/coubs/{coub_id}/upload_audio")
        return self.authenticated_request(
            "post", url, data=open(audio_path, "rb"), headers=headers
        ).json()

    def finalize_upload(
        self,
        coub_id: int,
        *,
        title: str,
        tags: List[str],
        visibility_type: VisibilityType = VisibilityType.PRIVATE,
        sound_enabled: bool = True,
    ):
        """
        Finalizing upload.
        
        Calling this method when all the editing is finished, and we can generate the final version for this coub.

        Resource endpoint:
            POST /api/v2/coubs/:id/finalize_upload

        :param coub_id: id from :mod: init_upload step
        :param title: the title of the coub;
        :param tags: tags assigned to the coub
        :param visibility_type: enum of the :mod: VisibilityType
        :param sound_enabled: enables or disables sound for the coub
        :return: {"status": "ok"} if if the request successed; {"message": "error"} otherwise
        
        >>> api.coubs.finalize_upload(93927327, title="Awesome CAT", tags=["cat", "animal"])
        {"status": "ok"}

        If all is well the finalization process starts. It usually takes 30–180 seconds.
        """
        url = self.build_url(f"/coubs/{coub_id}/finalize_upload")
        params = {
            "sound_enabled": sound_enabled,
            "title": title,
            "original_visibility_type": visibility_type,
            "tags": ",".join(tags),
        }
        return self.authenticated_request("post", url, params=params).json()

    def get_upload_status(self, coub_id: int):
        url = self.build_url(f"/coubs/{coub_id}/finalize_status")
        return self.authenticated_request("get", url).json()
