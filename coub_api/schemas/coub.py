from typing import Dict, List, Union, Optional
from datetime import date, datetime

from pydantic import AnyUrl, BaseModel

from .constants import Category, BigCoubType, ServiceType, SmallCoubType, VisibilityType

__all__ = ("BigCoub", "SmallCoub", "CoubTags")


class Categories(BaseModel):
    id: int
    title: str
    permalink: Category
    big_image_url: str
    small_image_url: str
    visible: bool
    subscriptions_count: int


class CoubTags(BaseModel):
    id: int
    title: str
    value: str


class Params(BaseModel):
    url: AnyUrl
    size: Optional[int]


# TODO
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
        video: str
        audio: Optional[List[AnyUrl]]

    html5: Html5
    mobile: Mobile


# TODO
class Communities(BaseModel):
    pass


class CoubAudioVersions(BaseModel):
    class Chunks(BaseModel):
        template: AnyUrl
        versions: List[str]
        chunks: List[int]

    template: AnyUrl
    versions: List[str]
    chunks: Chunks


class CoubImageVersion(BaseModel):
    template: AnyUrl
    versions: List[str]


class CoubFirstFrameVersion(BaseModel):
    template: AnyUrl
    versions: List[str]


class CoubExternalDownload(BaseModel):
    type: ServiceType
    service_name: str
    url: AnyUrl
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
        url: Optional[AnyUrl]
        image: Optional[AnyUrl]
        image_retina: Optional[AnyUrl]
        meta: Meta
        duration: Optional[float]
        amazon_url: Optional[AnyUrl]
        google_play_url: Optional[AnyUrl]
        bandcamp_url: Optional[AnyUrl]
        soundcloud_url: Optional[AnyUrl]
        track_name: Optional[str]
        track_artist: Optional[str]
        track_album: Optional[str]
        itunes_url: Optional[AnyUrl]

    class ExternalVideo(BaseModel):
        class Meta(BaseModel):
            service: ServiceType
            duration: float

        id: int
        title: Optional[str]
        url: Optional[AnyUrl]
        image: Optional[AnyUrl]
        image_retina: Optional[AnyUrl]
        meta: Meta
        duration: float
        raw_video_id: Optional[int]
        has_embed: Optional[bool]

    class RemixedFromCoubs(BaseModel):
        class Meta(BaseModel):
            duration: float

        id: int
        title: str
        url: Optional[AnyUrl]
        image: Optional[AnyUrl]
        image_retina: Optional[AnyUrl]
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
    audio_file_url: Optional[AnyUrl]
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

    id: int
    type: BigCoubType
    title: str
    permalink: str
    abuses: Optional[bool]
    visibility_type: VisibilityType
    audio_file_url: Optional[AnyUrl]
    channel_id: int
    created_at: datetime
    updated_at: datetime
    is_done: bool
    duration: float
    views_count: int
    cotd: Optional[bool]
    cotd_at: Optional[date]
    recoub: Optional[bool]
    like: Optional[bool]
    recoubs_count: int
    likes_count: int
    recoub_to: Optional[SubCoub]
    flag: Optional[bool]
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
    dislikes_count: int
    normalize_change_allowed: bool
    promoted_id: Optional[str]
    visible_on_explore: bool
    visible_on_explore_root: bool
    communities: List[Communities]
    # not documented or available for non-auth
    application: Optional[bool]
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
        template: AnyUrl
        versions: List[str]

    id: int
    type: SmallCoubType
    permalink: str
    title: str
    channel: ChannelSmall
    image_versions: ImageVersions


class SchemalessBigCoub(BaseModel):
    pass
