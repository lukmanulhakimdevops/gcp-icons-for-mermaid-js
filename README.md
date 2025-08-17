<!--
Copyright (c) 2020 David Holsgrove
Copyright 2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT (For details, see https://github.com/awslabs/aws-plantuml-icons/blob/master/LICENSE)
-->
# GCP Icons for PlantUML

PlantUML sprites, macros, and other includes for Google Cloud Platform (GCP) services and resources. Used to create PlantUML diagrams with GCP components. All elements are generated from the official [GCP Architecture Icons](https://cloud.google.com/icons) and when combined with [PlantUML](http://plantuml.com/) and the [C4 model](https://c4model.com/), are a great way to communicate your design, deployment, and topology as code.

Besides usage as custom sprites on PlantUML components, different types of diagrams can quickly and easily created created with the icons.

**This repository is a GCP Fork of the [AWS Icons for PlantUML](https://github.com/awslabs/aws-icons-for-plantuml) repository for creating pattens used in quality diagrams.**

## Table of Contents

<!-- toc -->

- [Getting Started](#getting-started)
  * [Hello World](#hello-world)
- [Examples](#examples)
  * [Basic Usage](#basic-usage)
  * [Raw Sprites](#raw-sprites)
  * [Simplified View](#simplified-view)
  * [Sequence Diagrams](#sequence-diagrams)
- [Distribution "Dist" Details](#distribution-dist-details)
- [Advanced Examples](#advanced-examples)
- [Customized Builds](#customized-builds)
- [Contributing](#contributing)
- [License Summary](#license-summary)
- [Acknowledgements](#acknowledgements)

<!-- tocstop -->

## Getting Started

In order to incorporate and use the *GCP Icons for PlantUML* resources, `!include` statements are added to your diagrams. A common include file/URL defines the base colors, styles, and characteristics for the diagram. Then additional configuration files can be added to further customize the diagram, followed by the elements used in the diagram.

To get started, include the `GCPCommon.puml` file from the `dist` directory in each `.puml` file or PlantUML diagram. This can be referenced by a URL directly to this repository, or by including the file locally. To use this repository, use the following:

<pre><code>!includeurl https://raw.githubusercontent.com/davidholsgrove/gcp-icons-for-plantuml/<b>v1.0</b>/dist/GCPCommon.puml
</code></pre>
This references the latest *GitHub release* version of the referenced file from GitHub when an Internet connection is available. You can also use the *master* branch by replacing `v1.0` (or which ever version you are using) with `master`.

All examples reference *master* and are designed with the most recent files. For consistency of UML diagrams when referencing the files directly via GitHub and not generated locally, it is recommended to use a specific release version.

For local access use `!include` instead of `!includeurl` and include the path to the file's location:

```bash
!include path/to/GCPCommon.puml
```

:exclamation: The `!includeurl` is deprecated in recent versions of PlantUML. Now `!include` can be used with local file paths *or* URLs. Please see the [Preprocessing](http://plantuml.com/preprocessing) notes for usage.

After inclusion of the `GCPCommon.puml` file, there are two different ways to reference resources:

1. **Use individual include files** - Use one file per service or setting. For example:

    `!incude GCPPuml/Storage/CloudStorage.puml`

1. **Use category include file** - Single include that contains all services and resources for that category. For example:

1. `!include GCPPuml/DeveloperTools/all.puml`

All of the services can be found in the `dist/` directory, which includes the service or product categories and the corresponding `puml` files.

For example, including these files from the repository (URL), the includes would look like this:

```bash
' Define the main location (URL or local file path)
!define GCPPuml https://raw.githubusercontent.com/davidholsgrove/gcp-icons-for-plantuml/master/dist
' Include main GCPCommon and then sprite files
!includeurl GCPPuml/GCPCommon.puml
!includeurl GCPPuml/DeveloperTools/all.puml
!includeurl GCPPuml/Storage/CloudStorage.puml
```

This defines the macro `GCPPuml` to point to the root of the `dist/` directory, which reduces the size of the include statements. Next the `GCPCommon.puml` file is loaded, and then the actual resource files. In this example, all of the entities in the *DeveloperTools* directory are added, and then only the *CloudStorage* entity from the *Storage* directory.

:exclamation: All examples reference the master *branch* of this repository. It is recommended that one of the release branches be used for documents. New releases will be created when GCP updates the GCP Architecture Icons. The release tag will be similar to the release date from GCP.

### Hello World

This is the [`examples/HelloWorld.puml`](<examples/HelloWorld.puml>) diagram code:

```bash
@startuml Hello World
!define GCPPuml https://raw.githubusercontent.com/davidholsgrove/gcp-icons-for-plantuml/master/dist
!includeurl GCPPuml/GCPCommon.puml
!includeurl GCPPuml/DeveloperTools/all.puml
!includeurl GCPPuml/Storage/CloudStorage.puml

actor "Person" as personAlias
CloudToolsforVisualStudio(desktopAlias, "Label", "Technology", "Optional Description")
CloudStorage(storageAlias, "Label", "Technology", "Optional Description")

personAlias --> desktopAlias
desktopAlias --> storageAlias

@enduml
```

This code generates the following diagram:

![](http://www.plantuml.com/plantuml/proxy?idx=0&src=https://raw.githubusercontent.com/davidholsgrove/gcp-icons-for-plantuml/master/examples/HelloWorld.puml)

## Examples

Below are some sample diagrams that demonstrate the uses of this repository by using different styles. The images are generated from the source diagram in the `examples` directory, which reference the PUML files in the `dist` directory of the main branch of this repository..

Consider these as starting points for how to use the resources in your own documents and diagrams. You may wish to use the sprites (images) in your UML diagrams, use the rectangle entities, or create large and complex C4 model diagrams.

### Basic Usage

This example shows GCP IoT processing of messages via the Rules Engine with an error action. It utilizes GCP service entities to show a simple architecture workflow. Each entity has a unique entity name and icon (`<<foo..>>`), name of function, and additional details or constraints. 

```bash
@startuml Basic Usage

!define GCPPuml https://raw.githubusercontent.com/davidholsgrove/gcp-icons-for-plantuml/master/dist
!includeurl GCPPuml/GCPCommon.puml
!includeurl GCPPuml/InternetOfThings/CloudIoTCore.puml
!includeurl GCPPuml/DataAnalytics/CloudPubSub.puml

left to right direction

agent "Published Event" as event #fff

CloudIoTCore(iotRule, "Action Error Rule", "error if Kinesis fails")
CloudPubSub(eventStream, "IoT Events", "2 shards")
CloudPubSub(errorQueue, "Rule Error Queue", "failed Rule actions")

event --> iotRule : JSON message
iotRule --> eventStream : messages
iotRule --> errorQueue : Failed action message

@enduml
```

This code generates the following diagram:

![](http://www.plantuml.com/plantuml/proxy?idx=0&src=https%3A%2F%2Fraw.githubusercontent.com%2Fdavidholsgrove%2Fgcp-icons-for-plantuml%2Fmaster%2Fexamples%2FBasic%2520Usage.puml)

### Raw Sprites

The individual icon sprites (complete list [here](GCPSymbols.md)) can be included in all diagrams. Here are few examples showing sprite usage on different entities (component, database, and GCP PlantUML).


```bash
@startuml Raw usage - Sprites

!define GCPPuml https://raw.githubusercontent.com/davidholsgrove/gcp-icons-for-plantuml/master/dist
!includeurl GCPPuml/GCPCommon.puml
!includeurl GCPPuml/AIAndMachineLearning/AIPlatform.puml
!includeurl GCPPuml/InternetOfThings/CloudIoTCore.puml

component "<color:green><$AIPlatform></color>" as myMLModel
database "<color:#232F3E><$CloudIoTCore></color>" as myRoboticService
CloudIoTCore(mySecondFunction, "Reinforcement Learning", "Gazebo")

rectangle "<color:GCP_SYMBOL_COLOR><$AIPlatform></color>" as mySecondML

myMLModel --> myRoboticService
mySecondFunction --> mySecondML

@enduml
```

This code generates the following diagram: 

![](http://www.plantuml.com/plantuml/proxy?idx=0&src=https%3A%2F%2Fraw.githubusercontent.com%2Fdavidholsgrove%2Fgcp-icons-for-plantuml%2Fmaster%2Fexamples%2FRaw%2520Sprite%2520Usage.puml)

### Simplified View

In some cases, PlantUML diagrams may contain too much information, but are still usable for executive or higher level conversations. Using the `GCPSimplified.puml` file filters out a lot of the technical details, while keeping the interactions between entities. Here is an example of a technical view and simplified view. To generate the simplified view, uncomment the `!define` statement and regenerate the image.

```bash
@startuml Two Modes - Technical View

!define GCPPuml https://raw.githubusercontent.com/davidholsgrove/gcp-icons-for-plantuml/master/dist
!include GCPPuml/GCPCommon.puml

' Include Material Design Common icons
!include <material/common>

' Uncomment the following line to create simplified view
!include GCPPuml/GCPSimplified.puml

!include GCPPuml/APIManagement/CloudEndpoints.puml
!include GCPPuml/Compute/AppEngine.puml
!include <material/cellphone_android>

left to right direction

GCPEntityColoring(MA_CELLPHONE_ANDROID)
MA_CELLPHONE_ANDROID(#9E9E9E, 1, sources, rectangle, "Android")
CloudEndpoints(endpoints, "GCP Cloud Endpoints", "api")
AppEngine(engine, "GCP App Engine", "API Backend Instances")

sources <--> endpoints
endpoints <--> engine

@enduml
```

This code generates the following diagram:

![](http://www.plantuml.com/plantuml/proxy?idx=0&src=https%3A%2F%2Fraw.githubusercontent.com%2Fdavidholsgrove%2Fgcp-icons-for-plantuml%2Fmaster%2Fexamples%2FTwo%2520Modes%2520-%2520Technical%2520View.puml)

And if the `!includeurl GCPPuml/GCPSimplified.puml`is uncommented, this simplified view is created:

![](http://www.plantuml.com/plantuml/proxy?idx=0&src=https%3A%2F%2Fraw.githubusercontent.com%2Fdavidholsgrove%2Fgcp-icons-for-plantuml%2Fmaster%2Fexamples%2FTwo%2520Modes%2520-%2520Simple%2520View.puml)

### Sequence Diagrams

Icons can also be used in UML sequence diagrams, either in full stereotype or by just using sprites and formatting via `participant` description.

## Customized Builds

It is also possible to customize the creation of the `dist/` PUML and PNG files. All details can be found in the [Generating the *PlantUML Icons for GCP* distribution documentation](scripts/README.md).

## License Summary

The icons provided in this package are made available to you under the terms of the CC-BY-ND 2.0 license, available in the `LICENSE` file. Code is made available under the MIT license in `LICENSE-CODE`.

## Acknowledgements

- [aws-icons-for-plantuml](https://github.com/awslabs/aws-icons-for-plantuml) - This repo is little more than a find / replace for AWS to GCP with small tweaks to take gcp icon folder structure!
# gcp-icons-for-mermaid-js
