from typing import Dict, List, Union, Optional
from datetime import date, datetime

from pydantic import UrlStr, BaseModel

from .constants import Category, BigCoubType, ServiceType, SmallCoubType, VisibilityType

__all__ = ("BigCoub", "SmallCoub", "CoubTags")


class Categories(BaseModel):
    id: int
    title: str
    permalink: Category


class CoubTags(BaseModel):
    id: int
    title: str
    value: str


class Params(BaseModel):
    url: UrlStr
    size: Optional[int]


class CoubFileVersion(BaseModel):
    class Html5(BaseModel):
        class Video(BaseModel):
            high: Optional[Params]
            med: Optional[Params]

        class Audio(BaseModel):
            high: Optional[Params]
            med: Optional[Params]
            sample_duration: Optional[float]

        video: Video
        audio: Optional[Audio]

    class Mobile(BaseModel):
        gifv: str
        audio: Optional[List[UrlStr]]

    html5: Html5
    mobile: Mobile


class CoubAudioVersions(BaseModel):
    class Chunks(BaseModel):
        template: UrlStr
        versions: List[str]
        chunks: List[int]

    template: UrlStr
    versions: List[str]
    chunks: Chunks


class CoubImageVersion(BaseModel):
    template: UrlStr
    versions: List[str]


class CoubFirstFrameVersion(BaseModel):
    template: UrlStr
    versions: List[str]


class CoubExternalDownload(BaseModel):
    type: ServiceType
    service_name: str
    url: UrlStr
    has_embed: bool


class CoubMediaBlocks(BaseModel):
    class AudioTrack(BaseModel):
        class Meta(BaseModel):
            year: Optional[str]
            album: Optional[str]
            title: Optional[str]
            artist: Optional[str]
            echonest_id: Optional[str]

        id: int
        title: str
        url: Optional[UrlStr]
        image: Optional[UrlStr]
        image_retina: Optional[UrlStr]
        meta: Meta
        duration: Optional[float]
        amazon_url: Optional[UrlStr]
        google_play_url: Optional[UrlStr]
        bandcamp_url: Optional[UrlStr]
        soundcloud_url: Optional[UrlStr]
        track_name: Optional[str]
        track_artist: Optional[str]
        track_album: Optional[str]
        itunes_url: Optional[UrlStr]

    class ExternalVideo(BaseModel):
        class Meta(BaseModel):
            service: ServiceType
            duration: float

        id: int
        title: Optional[str]
        url: Optional[UrlStr]
        image: Optional[UrlStr]
        image_retina: Optional[UrlStr]
        meta: Meta
        duration: float
        raw_video_id: Optional[int]
        has_embed: Optional[bool]

    class RemixedFromCoubs(BaseModel):
        class Meta(BaseModel):
            duration: float

        id: int
        title: str
        url: Optional[UrlStr]
        image: Optional[UrlStr]
        image_retina: Optional[UrlStr]
        meta: Meta
        duration: Optional[float]
        coub_channel_title: Optional[str]
        coub_channel_permalink: Optional[str]
        coub_views_count: Optional[int]
        coub_permalink: Optional[str]

    uploaded_raw_videos: List[dict]  # TODO
    external_raw_videos: List[ExternalVideo]
    remixed_from_coubs: List[RemixedFromCoubs]
    external_video: Optional[ExternalVideo]
    audio_track: Optional[AudioTrack]


class SubCoub(BaseModel):
    from .channel import ChannelSmall

    id: int
    audio_file_url: Optional[UrlStr]
    type: BigCoubType
    permalink: str
    title: str
    visibility_type: VisibilityType
    channel_id: int
    is_done: bool
    created_at: datetime
    updated_at: datetime
    views_count: int
    cotd: Optional[bool]
    cotd_at: Optional[date]
    recoub: Optional[bool]
    like: Optional[bool]
    recoub_to: Optional[dict]
    original_sound: bool
    has_sound: bool
    file_versions: CoubFileVersion
    audio_versions: Union[CoubAudioVersions, dict]
    image_versions: Union[CoubImageVersion, dict]
    first_frame_versions: CoubFirstFrameVersion
    dimensions: Dict[str, List[int]]
    age_restricted: bool
    allow_reuse: bool
    banned: bool
    external_download: Union[bool, CoubExternalDownload]
    channel: ChannelSmall

    # not documented or available for non-auth
    favourite: Optional[bool]
    flag: Optional[bool]
    published: Optional[bool]
    age_restricted_by_admin: Optional[bool]
    published_at: Optional[datetime]
    is_editable: Optional[bool]
    page_w_h: Optional[List[int]]
    global_safe: Optional[bool]
    site_w_h: Optional[List[int]]
    site_w_h_small: Optional[List[int]]


# see https://coub.com/dev/docs/data+structures/coub+big+json
class BigCoub(BaseModel):
    from .channel import ChannelSmall

    abuses: Optional[bool]
    audio_file_url: Optional[UrlStr]
    id: int
    type: BigCoubType
    permalink: str
    title: str
    visibility_type: VisibilityType
    channel_id: int
    is_done: bool
    created_at: datetime
    updated_at: datetime
    duration: float
    views_count: int
    cotd: Optional[bool]
    cotd_at: Optional[date]
    recoub: bool
    like: bool
    recoubs_count: int
    likes_count: int
    recoub_to: Optional[SubCoub]
    original_sound: bool
    has_sound: bool
    file_versions: CoubFileVersion
    audio_versions: Union[CoubAudioVersions, dict]
    image_versions: Union[CoubImageVersion, dict]
    first_frame_versions: Union[CoubFirstFrameVersion, dict]
    dimensions: Dict[str, Optional[List[int]]]
    age_restricted: bool
    allow_reuse: bool
    banned: bool
    external_download: Union[bool, CoubExternalDownload]
    channel: ChannelSmall
    percent_done: int
    tags: List[CoubTags]
    raw_video_id: Union[int, str]
    media_blocks: CoubMediaBlocks
    raw_video_thumbnail_url: str
    raw_video_title: Optional[str]
    video_block_banned: bool
    audio_copyright_claim: Optional[str]
    categories: List[Categories]

    # not documented or available for non-auth
    flag: Optional[bool]
    published: Optional[bool]
    age_restricted_by_admin: Optional[bool]
    published_at: Optional[datetime]
    is_editable: Optional[bool]
    page_w_h: Optional[List[int]]
    global_safe: Optional[bool]
    site_w_h: Optional[List[int]]
    site_w_h_small: Optional[List[int]]


# see https://coub.com/dev/docs/data+structures/channel+small+json
class SmallCoub(BaseModel):
    from .channel import ChannelSmall

    class ImageVersions(BaseModel):
        template: UrlStr
        versions: List[str]

    id: int
    type: SmallCoubType
    permalink: str
    title: str
    channel: ChannelSmall
    image_versions: ImageVersions
