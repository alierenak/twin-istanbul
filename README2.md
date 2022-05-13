# Twin Istanbul - A digital twin project for smart cities

**Acknowledgement -** *Twin Istanbul Project is developed during the [Sustainability Hackathon for Smart Cities](https://surdurulebilirsehirler.ist) with the support of [Microsoft Turkey](https://www.microsoft.com/tr-tr) and [Istanbul Metropolitan Municipality (IMM)](http://ibb.istanbul/). Special thanks to them for organizing this event!*

<h4> Abstract </h4> The condition of roads, bridges, metro lines and other transportation components dramatically influences the economy’s ability to function and grow. While metropolia keep growing, it is very challenging to maintain them at scale for crowds. Public resources are scarce, and it is tough to manage investments accordingly. This project is aimed to establish a digital twin of the Istanbul transportation network, which will be a platform to forecast, plan and organize public investments with the genuine involvement of citizens democratically. The project intersects with the current <a href="https://www.ibb.istanbul/Uploads/2020/2/iBB-STRATEJIK-PLAN-2020-2024.pdf">Strategic Plan of the IMM</a> about making Istanbul accessible and smart. Moreover, it will strengthen and accelerate the digital transformation in the city administration. 

<h4> Problem Description </h4> Istanbul is the most crowded city in Europe with its more than 15 million population. Chronic traffic congestion, rising motorization, overloaded public transit services, and air and noise pollution are all issues that urban transportation is struggling with. With unusual public events such as sports competitions, concerts and crowd events, mobility is increasing, and the challenge is getting hard. From 2016 to 2022, more than **US$ 36 billion** was spent on large transportation projects such as Euroasia Tunnel, Grand Istanbul Tunnel, 3rd Bosphorus bridge and more. However, clean and sustainable transport modes for Istanbul, e.g. cycling, walking and public transportation, are not effectively used and are still far from the objective. According to <a href="https://assets.new.siemens.com/siemens/assets/api/uuid:fddc99e7-5907-49aa-92c4-610c0801659e/european-green-city-index.pdf"> European Green City Index</a>, Istanbul is 16th at CO2 emission rank, 23th at urban transportation index and 23th air quality measure across 30 european country. In order to make Istanbul more sustainable and green, there is a need for a comprehensive strategic plan and infrastructural investments. 

<h4> Available Solutions </h4> Currently, investments and projects are planned according to travel demand. The approach is called "predict and provide" in the transport literature, and it is unsustainable, static and inefficient. Moreover, plans and projects depend on managers who are continuously changed due to the nature of politics. Data-driven approaches have been developed in recent years. Many approaches recognize patterns in individual mobility and activity choices, build large scale networks, make analyses of the spatiotemporal dataset, forecast road traffic and travel demand, and develop recommendation algorithms for smart routing and trip planning. However, current data-driven strategies are not continuous and primarily human-made. Simulations require advanced platforms and a large amount of data, which do not exist most of the time. Also, urban planning is a complex task, and events are consequently related to each other. The Director of the Strategy Development Department in IETT stated that the crowded bus and minibus services encourage people to own and use more cars, which causes more traffic congestion. On the other hand, private transportation services are profit-focused and do not tend to support a capacity increase due to potential falls.

<h4> Proposed Model </h4> We are proposing a digital twin concept to plan and organize public decisions with the involvement of citizens democratically. <a href="https://docs.microsoft.com/en-us/azure/digital-twins"> Azure Digital Twin Description Langauge </a> will be used to declare and deploy Twin Istanbul. At first, we will use transportation data to conduct domain-specific digital twins. We believe Digital Twin is a promising concept for creating a data-driven decision framework. It will enable future planning, development, and data analysis. More importantly, It will give decision-makers more insight into the city itself, such as how smart city utilities are distributed and consumed. In order to achieve that, Open Data Portal by IMM will be used. IMM releases public data about Istanbul for citizens and developers on this platform. There are more than 90 datasets about mobility, and more are available upon request. According to <a href="https://www.ibb.istanbul/Uploads/2020/2/iBB-STRATEJIK-PLAN-2020-2024.pdf"> Strategic Plan of the IMM <a> - A1H7, it is aimed to develop 3D digital model of Istanbul, increase available dataset in Open Data Portal and complete geopraphical data infrasturce. 

<h4> How to run? </h4> 
  1. Define your Azure .env variables in `variables.env`. File format should exactly be like;
  ```json
  {
    "AZURE_URL": <digital-twin-host-url>,
    "AZURE_TENANT_ID": <your-tenant-id>,
    "AZURE_CLIENT_ID": <app registration client id>,
    "AZURE_CLIENT_SECRET": <app client id>,
    "SUBSCRIPTION_KEY": <subscription key>
  }
  ```
 
  2. Create your virtual python environment
  3. `pip3 install -r requirements.txt`
  4. python3 main.py

<h4> Important informations </h4> Inside main function, there are 2 thread running simultaneously. One of them is extracting traffic data from Azure Maps and NEVER STOPs. Until application is shutted down, it will continue to extract data. Another one is downloading and preprocessing data, creating digital twin and analysing data. It also ends with infinite while loop which listens data.
  
  
   



