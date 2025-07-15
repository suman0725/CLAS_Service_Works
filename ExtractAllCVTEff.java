import org.jlab.groot.data.TDirectory;
import org.jlab.groot.data.GraphErrors;
import java.io.PrintWriter;

public class ExtractAllCVTEff {
    public static void main(String[] args) {
        if (args.length < 1) {
            System.out.println("Usage: java ExtractAllCVTEff <hipo_file>");
            System.exit(1);
        }
        String hipoFile = args[0];
        TDirectory reader = new TDirectory();
        try {
            reader.readFile(hipoFile);
        } catch (Exception e) {
            System.err.println("Error opening HIPO file: " + e.getMessage());
            System.exit(1);
        }

        for (int sector = 1; sector <= 3; sector++) {
            for (int layer = 1; layer <= 6; layer++) {
                String histName = "/timelines/S" + sector + "L" + layer;
                GraphErrors graph = (GraphErrors) reader.getObject(histName);
                if (graph == null) {
                    System.out.println("Histogram " + histName + " not found!");
                    continue;
                }
                try (PrintWriter writer = new PrintWriter("/w/hallb-scshelf2102/clas12/suman/SW_25/efficiency_s" + sector + "_l" + layer + ".txt")) {
                    writer.println("RunNumber\tEfficiency");
                    for (int i = 0; i < graph.getDataSize(0); i++) {
                        double runNumber = graph.getDataX(i);
                        double efficiency = graph.getDataY(i);
                        writer.println(runNumber + "\t" + efficiency);
                    }
                } catch (Exception e) {
                    System.err.println("Error writing file for S" + sector + " L" + layer + ": " + e.getMessage());
                }
            }
        }
    }
}