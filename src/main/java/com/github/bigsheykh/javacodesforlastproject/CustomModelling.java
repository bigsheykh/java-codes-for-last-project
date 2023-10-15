package com.github.bigsheykh.javacodesforlastproject;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

import org.apache.maven.model.Model;
import org.apache.maven.model.building.DefaultModelBuilder;
import org.apache.maven.model.building.DefaultModelBuilderFactory;
import org.apache.maven.model.building.Result;
import org.apache.maven.shared.invoker.DefaultInvocationRequest;
import org.apache.maven.shared.invoker.DefaultInvoker;
import org.apache.maven.shared.invoker.InvocationRequest;
import org.apache.maven.shared.invoker.MavenInvocationException;
import org.apache.maven.shared.invoker.PrintStreamLogger;
import org.codehaus.plexus.util.ReaderFactory;
import org.codehaus.plexus.util.xml.Xpp3Dom;
import org.codehaus.plexus.util.xml.Xpp3DomBuilder;



public class CustomModelling {
    DefaultModelBuilder defaultModelBuilder;


    public static String getBaseDir() {
        final String path = System.getProperty( "basedir" );
        return null != path ? path : new File( "" ).getAbsolutePath();
    }

    public CustomModelling(File pomFile) {
        DefaultModelBuilderFactory defaultModelBuilderFactory = new DefaultModelBuilderFactory();
        defaultModelBuilder = defaultModelBuilderFactory.newInstance();
        Result<? extends Model> rawModels = defaultModelBuilder.buildRawModel(pomFile, 0, true);
        Model model = rawModels.get();
        System.out.println(model.getGroupId());
        System.out.println(model.getName());
        System.out.println(model.getId());
        System.out.println(model.getVersion());
        System.out.println(model.getModelVersion());
        InvocationRequest req = new DefaultInvocationRequest();
        req.setPomFile( pomFile );
        List<String> goalList = new ArrayList<>();
        goalList.add("dependency:tree");
        goalList.add("help:effective-pom");
        req.setGoals(goalList);
        DefaultInvoker invoker = new DefaultInvoker();
        invoker.setLogger(new GoodLogger());
        try {
            invoker.execute( req );
            invoker.getLogger();
        } catch (MavenInvocationException e) {
            e.printStackTrace();
        }        
    }

    public class GoodLogger
        extends PrintStreamLogger
    {

        /**
         * Creates a new logger with a threshold of {@link #INFO}.
         */
        public GoodLogger()
        {
            super( System.out, INFO );
        }

    }

    public class NewTreeMojo {
        String artifactId;
        String groupId;
        String version;

        NewTreeMojo(File testPom, Model model) {
            try {
                Xpp3Dom pluginPomDom = Xpp3DomBuilder.build(ReaderFactory.newXmlReader(testPom));
                artifactId = pluginPomDom.getChild("artifactId").getValue();
                groupId = resolveFromRootThenParent(pluginPomDom, "groupId");
                version = resolveFromRootThenParent(pluginPomDom, "version");
                System.out.println(pluginPomDom.toString());
            } catch (Exception e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }

        private String resolveFromRootThenParent(Xpp3Dom pluginPomDom, String element) throws Exception {
            Xpp3Dom elementDom = pluginPomDom.getChild(element);
    
            // parent might have the group Id so resolve it
            if (elementDom == null) {
                Xpp3Dom pluginParentDom = pluginPomDom.getChild("parent");
    
                if (pluginParentDom != null) {
                    elementDom = pluginParentDom.getChild(element);
                    if (elementDom == null) {
                        throw new Exception("unable to determine " + element);
                    }
                    return elementDom.getValue();
                }
                throw new Exception("unable to determine " + element);
            }
            return elementDom.getValue();
        }
    }

}
