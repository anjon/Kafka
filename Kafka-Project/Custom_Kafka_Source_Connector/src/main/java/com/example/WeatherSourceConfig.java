package com.example;

import org.apache.kafka.common.config.AbstractConfig;
import org.apache.kafka.common.config.ConfigDef;

import java.util.Map;

public class WeatherSourceConfig extends AbstractConfig {

    public static final String API_KEY = "openweather.api.key";
    public static final String CITY = "openweather.city";
    public static final String TOPIC = "kafka.topic";
    public static final String POLL_INTERVAL = "poll.interval.ms";

    public static final ConfigDef CONFIG_DEF = new ConfigDef()
            .define(API_KEY, ConfigDef.Type.STRING, ConfigDef.Importance.HIGH, "OpenWeather API Key")
            .define(CITY, ConfigDef.Type.STRING, ConfigDef.Importance.HIGH, "City name")
            .define(TOPIC, ConfigDef.Type.STRING, ConfigDef.Importance.HIGH, "Kafka topic")
            .define(POLL_INTERVAL, ConfigDef.Type.INT, 60000, ConfigDef.Importance.MEDIUM, "Polling interval");

    public WeatherSourceConfig(Map<String, String> props) {
        super(CONFIG_DEF, props);
    }
}