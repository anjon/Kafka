package org.example.avro.specific;

import com.example.Customer;
import org.apache.avro.file.DataFileReader;
import org.apache.avro.file.DataFileWriter;
import org.apache.avro.io.DatumReader;
import org.apache.avro.io.DatumWriter;
import org.apache.avro.specific.SpecificDatumReader;
import org.apache.avro.specific.SpecificDatumWriter;

import java.io.File;
import java.io.IOException;

public class SpecificRecordExamples {
    public static void main(String[] args) {

        // step 1 : create specific record
        Customer.Builder customerBuilder = Customer.newBuilder();
        customerBuilder.setAge(35);
        customerBuilder.setFirstName("Anjon");
        customerBuilder.setLastName("Sarker");
        customerBuilder.setHeight(172f);
        customerBuilder.setWeight(95.5f);
        //customerBuilder.setAutomatedEmail(false);
        Customer customer = customerBuilder.build();

        System.out.println(customer);

        // step 2 : write to file
        final DatumWriter<Customer> datumWriter = new SpecificDatumWriter<>(Customer.class);

        try (DataFileWriter<Customer> dataFileWriter = new DataFileWriter<>(datumWriter)) {
            dataFileWriter.create(customer.getSchema(), new File("customer-specific.avro"));
            dataFileWriter.append(customer);
            System.out.println("Successfully wrote customer-specific.avro");
        } catch (IOException e) {
            e.printStackTrace();
        }

        // step 3 : read from file
        final File file = new File("customer-specific.avro");
        final DatumReader<Customer> datumReader = new SpecificDatumReader<>(Customer.class);
        final DataFileReader<Customer> dataFileReader;
        try {
            System.out.println("Reading our specific record");
            dataFileReader = new DataFileReader<>(file, datumReader);
            while (dataFileReader.hasNext()) {
                Customer readCustomer = dataFileReader.next();
                // step 4 : interpret
                System.out.println(readCustomer.toString());
                System.out.println("First Name: " + readCustomer.getFirstName());
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

    }
}
