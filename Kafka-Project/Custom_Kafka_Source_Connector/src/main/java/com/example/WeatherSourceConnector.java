package com.example;

import org.apache.kafka.connect.connector.Task;
import org.apache.kafka.connect.source.SourceConnector;
import org.apache.kafka.common.config.ConfigDef;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

//import java.util.*;

public class WeatherSourceConnector extends SourceConnector {

    private Map<String, String> configProps;

    @Override
    public void start(Map<String, String> props) {
        this.configProps = props;
    }

    @Override
    public Class<? extends Task> taskClass() {
        return WeatherSourceTask.class;
    }

    @Override
    public List<Map<String, String>> taskConfigs(int maxTasks) {
        List<Map<String, String>> configs = new ArrayList<>();
        configs.add(configProps);
        return configs;
    }

    @Override
    public void stop() {
        // nothing
    }

    @Override
    public ConfigDef config() {
        return WeatherSourceConfig.CONFIG_DEF;
    }

    @Override
    public String version() {
        return "1.1";
    }
}