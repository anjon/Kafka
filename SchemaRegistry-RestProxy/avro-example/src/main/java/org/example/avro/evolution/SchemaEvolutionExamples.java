package org.example.avro.evolution;

public class SchemaEvolutionExamples {

    public static void main(String[] args) {

        // Let's test a backward compatible read
        // we deal with the V1 of our customer
        CustomerV1 customerV1 = CustomerV1.newBuilder()
                .setAge(34)
                .setAutomatedEmail(false)
                .setFirstName("John")
                .setLastName("Doe")
                .setHeight(178f)
                .setWeight(75f)
                .build();
        System.out.println("Customer V1 = " + customerV1.toString());
    }
}
