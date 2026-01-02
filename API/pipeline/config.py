import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
API_ROOT = PROJECT_ROOT / "API"

PITCH_LENGTH_M = 105.0
PITCH_WIDTH_M = 68.0

TARGET_FPS = 25
DEFAULT_FPS = 25

DETECTION_CONFIDENCE_THRESHOLD = 0.5
YOLO_MODEL_PATH = API_ROOT / "models" / "yolov8l.pt"
YOLO_DEVICE = "cuda"

TRACKER_TYPE = "ocsort"
MAX_TRACK_AGE = 30
MIN_TRACK_HITS = 3

TEAM_KMEANS_CLUSTERS = 2
TEAM_UPPER_BODY_RATIO = 0.4
TEAM_CACHE_SIZE = 100

CALIBRATION_DIR = API_ROOT / "calibration" / "matrices"
DEFAULT_HOMOGRAPHY_PATH = CALIBRATION_DIR / "default_homography.npy"

MIN_X_COORDINATE = 0.0
MAX_X_COORDINATE = PITCH_LENGTH_M
MIN_Y_COORDINATE = 0.0
MAX_Y_COORDINATE = PITCH_WIDTH_M

MAX_PLAYER_SPEED_MPS = 10.0
MIN_CONFIDENCE = 0.5

REQUIRE_TEAM_ASSIGNMENT = True

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "soccer_tracking"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}

DB_CONNECTION_STRING = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
    f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
)

DB_BATCH_SIZE = 1000
DB_COMMIT_INTERVAL = 5000

TARGET_PROCESSING_FPS = 10
COORDINATE_ERROR_THRESHOLD_M = 1.5

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = PROJECT_ROOT / "logs"
LOG_FILE = LOG_DIR / "pipeline.log"

LOG_PERFORMANCE_INTERVAL = 100
LOG_VALIDATION_FAILURES = True

OUTPUT_DIR = PROJECT_ROOT / "outputs"
RESULTS_DIR = OUTPUT_DIR / "results"
VISUALIZATIONS_DIR = OUTPUT_DIR / "visualizations"

DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
SAVE_DEBUG_FRAMES = DEBUG_MODE
DEBUG_FRAME_DIR = OUTPUT_DIR / "debug_frames"

def validate_config():
    if not DB_CONFIG["password"] and not DEBUG_MODE:
        raise ValueError("Database password not set. Please set DB_PASSWORD environment variable.")

    if PITCH_LENGTH_M <= 0 or PITCH_WIDTH_M <= 0:
        raise ValueError("Pitch dimensions must be positive")

    if TARGET_FPS <= 0 or TARGET_FPS > 120:
        raise ValueError("TARGET_FPS must be between 1 and 120")

    if not 0 <= DETECTION_CONFIDENCE_THRESHOLD <= 1:
        raise ValueError("DETECTION_CONFIDENCE_THRESHOLD must be between 0 and 1")

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    CALIBRATION_DIR.mkdir(parents=True, exist_ok=True)

    if SAVE_DEBUG_FRAMES:
        DEBUG_FRAME_DIR.mkdir(parents=True, exist_ok=True)


if __name__ != "__main__":
    try:
        validate_config()
    except ValueError as e:
        print(f"Warning: Configuration validation failed: {e}")
