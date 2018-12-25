from enum import Enum, unique


@unique
class Section(str, Enum):
    HOT = "hot"
    RANDOM = "random"
    NEWEST = "fresh"
    RISING = "rising"


@unique
class Period(str, Enum):
    DAILY = ""
    MONTHLY = "monthly"
    WEEKLY = "weekly"
    QUARTER = "quarter"
    HALF_YEAR = "half"


@unique
class Category(str, Enum):
    ALL = ""
    ANIMALS = "animals-pets"
    MASHUP = "mashup"
    ANIME = "anime"
    MOVIES = "movies"
    GAMING = "gaming"
    CARTOONS = "cartoons"
    ART = "art"
    MUSIC = "music"
    SPORTS = "sports"
    SCIENCE = "science-technology"
    CELEBRITY = "celebrity"
    NATURE = "nature-travel"
    FASHION = "fashion"
    CARS = "cars"
    NSFW = "nsfw"
    DANCE = "dance"
    NEWS = "news"
    ARCHITECTURE = "architecture"
    OMG = "omg"
    TV_SERIES = "tv-series"
    WTF = "wtf"
    FUNNY = "funny"
    LIVE = "live"
    FOOD = "food"
    GEEK = "geek"
    PERFECT_LOOP = "perfect-loop"


@unique
class VisibilityType(str, Enum):
    PUBLIC = "public"
    FRIENDS = "friends"
    UNLISTED = "unlisted"
    PRIVATE = "private"


@unique
class BigCoubType(str, Enum):
    default = "Coub::Simple"
    recoub = "Coub::Recoub"


@unique
class SmallCoubType(str, Enum):
    default = "Coub::Simple"
    temp = "Coub::Temp"
    recoub = "Coub::Recoub"


@unique
class Provider(str, Enum):
    FACEBOOK = "facebook"
    TWITTER = "twitter"
    VKONTAKTE = "vkontakte"
    GOOGLE = "google"


@unique
class ServiceType(str, Enum):
    YOUTUBE = "Youtube"
    VIMEO = "Vimeo"
    VK = "Vk"
    INSTAGRAM = "Instagram"
    VINE = "Vine"
    WIMP = "Wimp"
    FACEBOOK = "Facebook"
    ODNOKLASSNIKI = "Odnoklassniki"
    FUNNYORDIE = "Funnyordie"
    CARAMBATV = "Carambatv"
    COLLEGEHUMOR = "CollegeHumor"
    LIVELEAK = "LiveLeak"
    DAILYMOTION = "Dailymotion"
    TETTV = "TetTv"
    TWITTER = "Twitter"
    TWITCH = "Twitch"
    TUMBLR = "Tumblr"
    GFYCAT = "Gfycat"
    IMGUR = "Imgur"
    GIPHY = "Giphy"
    REDDIT = "Reddit"
    # UNKNOWN
    URLDOWNLOAD = "UrlDownload"
