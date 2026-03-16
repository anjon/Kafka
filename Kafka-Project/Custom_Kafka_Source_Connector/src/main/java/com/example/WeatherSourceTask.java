package com.example;

import org.apache.kafka.connect.source.SourceTask;
import org.apache.kafka.connect.source.SourceRecord;

import org.apache.kafka.connect.data.Schema;
import org.apache.kafka.connect.data.SchemaBuilder;
import org.apache.kafka.connect.data.Struct;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;

import java.util.*;

public class WeatherSourceTask extends SourceTask {

    private WeatherSourceConfig config;
    private OpenWeatherClient client;

    private static final Schema WEATHER_SCHEMA = SchemaBuilder.struct()
            .name("weather")
            .field("city", Schema.STRING_SCHEMA)
            .field("latitude", Schema.FLOAT64_SCHEMA)
            .field("longitude", Schema.FLOAT64_SCHEMA)
            .field("temperature", Schema.FLOAT64_SCHEMA)
            .field("feels_like", Schema.FLOAT64_SCHEMA)
            .field("humidity", Schema.INT32_SCHEMA)
            .field("weather", Schema.STRING_SCHEMA)
            .field("wind_speed", Schema.FLOAT64_SCHEMA)
            .field("timestamp", Schema.INT64_SCHEMA)
            .build();

    @Override
    public void start(Map<String, String> props) {
        config = new WeatherSourceConfig(props);
        client = new OpenWeatherClient();
    }

    @Override
    public List<SourceRecord> poll() {

        List<SourceRecord> records = new ArrayList<>();

        try {

            String city = config.getString(WeatherSourceConfig.CITY);
            String apiKey = config.getString(WeatherSourceConfig.API_KEY);
            String topic = config.getString(WeatherSourceConfig.TOPIC);
            int interval = config.getInt(WeatherSourceConfig.POLL_INTERVAL);

            String raw = client.fetchWeather(city, apiKey);

            ObjectMapper mapper = new ObjectMapper();
            JsonNode root = mapper.readTree(raw);

            double lat = root.path("coord").path("lat").doubleValue();
            double lon = root.path("coord").path("lon").doubleValue();

            double temp = root.path("main").path("temp").doubleValue();
            double feels = root.path("main").path("feels_like").doubleValue();
            int humidity = root.path("main").path("humidity").intValue();

            double wind = root.path("wind").path("speed").doubleValue();

            String description =
                    root.path("weather").isArray() && !root.path("weather").isEmpty()
                            ? root.path("weather").get(0).path("description").asString()
                            : "unknown";

            long timestamp = root.path("dt").longValue();

            Struct weatherStruct = new Struct(WEATHER_SCHEMA)
                    .put("city", city)
                    .put("latitude", lat)
                    .put("longitude", lon)
                    .put("temperature", temp)
                    .put("feels_like", feels)
                    .put("humidity", humidity)
                    .put("weather", description)
                    .put("wind_speed", wind)
                    .put("timestamp", timestamp);

            SourceRecord record = new SourceRecord(
                    Collections.singletonMap("partition", city),
                    Collections.singletonMap("offset", System.currentTimeMillis()),
                    topic,
                    null,
                    null,
                    WEATHER_SCHEMA,
                    weatherStruct
            );

            records.add(record);

            Thread.sleep(interval);

        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }

        return records;
    }

    @Override
    public void stop() {}

    @Override
    public String version() {
        return "1.1";
    }
}