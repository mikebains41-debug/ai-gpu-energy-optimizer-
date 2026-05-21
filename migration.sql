CREATE TABLE IF NOT EXISTS gpu_metrics (
    time            TIMESTAMPTZ      NOT NULL,
    gpu_id          TEXT             NOT NULL,
    node_id         TEXT             NOT NULL,
    power_watts     DOUBLE PRECISION,
    gpu_util        DOUBLE PRECISION,
    mem_util        DOUBLE PRECISION,
    temp_c          DOUBLE PRECISION,
    ghost_flag      BOOLEAN          DEFAULT FALSE,
    desync_flag     BOOLEAN          DEFAULT FALSE,
    cei_score       DOUBLE PRECISION,
    mem_clock_mhz   INTEGER,
    p_state         INTEGER,
    PRIMARY KEY (time, gpu_id)
);
SELECT create_hypertable('gpu_metrics','time',chunk_time_interval => INTERVAL '1 day',if_not_exists => TRUE);
CREATE INDEX IF NOT EXISTS idx_gpu_id ON gpu_metrics (gpu_id, time DESC);
CREATE INDEX IF NOT EXISTS idx_ghost  ON gpu_metrics (ghost_flag, time DESC) WHERE ghost_flag = TRUE;
CREATE INDEX IF NOT EXISTS idx_desync ON gpu_metrics (desync_flag, time DESC) WHERE desync_flag = TRUE;
