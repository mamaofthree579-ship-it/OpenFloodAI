import json, random
from datetime import datetime

# 🌎 Global region structure (continent → country → state/province → county/metro)
REGION_STRUCTURE = {
    "North America": {
        "United States": {
    "Alabama": ["Jefferson County", "Mobile County", "Madison County", "Autauga County", "Baldwin County", "Barbour County", "Bibb County", "Blount County", "Bullock County", "Butler County", "Calhoun County", "Chambers Count", "Cherokee County", "Chilton County", "Choctaw County", "Clarke County", "Clay County", "Cleburne County", "Coffee County", "Colbert County", "Conecuh County", "Coosa County", "Covington County", "Crenshaw County", "Cullman County", "Dale County", "Dallas County", "DeKalb County", "Elmore County", "Escambia County", "Etowah County", "Fayette County", "Franklin County", "Geneva Count", "Greene County", "Hale County", "Henry County", "Houston County", "Jackson County", "Lamar County", "Lauderdale County", "Lawrence County", "Lee County", "Limestone County", "Lowndes County", "Macon County", "Marengo County", "Marion County", "Marshall County", "Monroe County", "Montgomery County", "Morgan County", "Perry County", "Pickens County", "Pike County", "Randolph County", "Russell County", "St. Clair County", "Shelby County", "Sumter County", "Talladega County", "Tallapoosa County", "Tuscaloosa County", "Walker County", "Washington County", "Wilcox County", "Winston County"],
    "Alaska": ["Anchorage Municipality", "Fairbanks North Star Borough", "Matanuska-Susitna Borough", "Aleutians East", "Aleutians West", "Bethel Borough", "Bristol Bay", "Chugach", "Copper River", "Denali", "Dillingham", "Hoonah-Angoon", "Kusilvak", "Bristol Bay Borough", "Denali Borough", "Haines Borough", "City and Borough of Juneau", "Kenai Peninsula", "Ketchikan Gateway", "Kodiak Island", "Lake and Peninsula", "Nome", "North Slope", "Northwest Arctic", "Prince of Wales-Hyder", "Southeast Fairbanks", "Skagway", "Valdez-Cordova Borough", "Wrangell City and Borough", "Yukon-Koyukuk Borough"],
    "Arizona": ["Maricopa County", "Pima County", "Pinal County", "Apache County", "Cochise County", "Coconino County", "Gila County", "Graham County", "Greenlee County", "La Paz County", "Mohave County", "Navajo County", "Santa Cruz County", "Yavapai County", "Yuma County"],
    "Arkansas": ["Pulaski County", "Benton County", "Washington County", "Arkansas County", "Ashley County", "Baxter County", "Boone County", "Bradley County", "Calhoun County", "Carroll County", "Chicot County", "Clark County", "Clay County", "Cleburne County", "Cleveland County", "Columbia County", "Conway County", "Craighead County", "Crawford County", "Crittenden County", "Cross County", "Dallas County", "Desha County", "Drew County", "Faulkner County", "Franklin County", "Fulton County", "Garland County", "Grant County", "Greene County", "Hempstead County", "Hot Spring County", "Howard County", "Independence County", "Izard County", "Jackson County", "Jefferson County", "Johnson County", "Lafayette County", "Lawrence County", "Lee County", "Lincoln County", "Little River County", "Logan County", "Lonoke County", "Madison County", "Marion County", "Miller County", "Mississippi County", "Monroe County", "Montgomery County", "Nevada County", "Newton County", "Ouachita County", "Perry County", "Phillips County", "Pike County", "Poinsett County", "Polk County", "Pope County", "Prairie County", "Randolph County", "Saint Francis County", "Saline County", "Scott County", "Searcy County", "Sebastian County", "Sevier County", "Sharp County", "Stone County", "Union County", "Van Buren County", "White County", "Woodruff County", "Yell County"],
    "California": ["Los Angeles County", "San Diego County", "Orange County", "Sacramento County", "San Francisco County", "Alameda County", "Alpine County", "Amador County", "Butte County", "Calaveras County", "Colusa County", "Contra Costa County", "Del Norte County", "El Dorado County", "Fresno County", "Glenn County", "Humboldt County", "Imperial County", "Inyo County", "Kern County", "Kings County", "Lake County", "Lassen County", "Madera County", "Marin County", "Mariposa County", "Mendocino County", "Merced County", "Modoc County", "Mono County", "Monterey County", "Napa County", "Nevada County", "Placer County", "Plumas County", "Riverside County", "San Benito County", "San Bernardino County", "San Diego County", "San Joaquin County", "San Luis Obispo County", "San Mateo County", "Santa Barbara County", "Santa Clara County", "Santa Cruz County", "Shasta County", "Sierra County", "Siskiyou County", "Solano County", "Sonoma County", "Stanislaus County", "Sutter County", "Tehama County", "Trinity County", "Tulare County", "Tuolumne County", "Ventura County", "Yolo County", "Yuba County"],
    "Colorado": ["Denver County", "El Paso County", "Arapahoe County", "Adams County", "Alamosa County", "Archuleta County", "Baca County", "Bent County", "Boulder County", "Broomfield County", "Chaffee County", "Cheyenne County", "Clear Creek County", "Conejos County", "Costilla County", "Crowley County", "Custer County", "Delta County", "Dolores County", "Douglas County", "Eagle County", "Elbert County", "Fremont County", "Garfield County", "Gilpin County", "Grand County", "Gunnison County", "Hinsdale County", "Huerfano County", "Jackson County", "Jefferson County", "Kiowa County", "Kit Carson County", "La Plata County", "Lake County", "Larimer County", "Las Animas County", "Lincoln County", "Logan County", "Mesa County", "Mineral County", "Moffat County", "Montezuma County", "Montrose County", "Morgan County", "Otero County", "Ouray County", "Park County", "Phillips County", "Pitkin County", "Prowers County", "Pueblo County", "Rio Blanco County", "Rio Grande County", "Routt County", "Saguache County", "San Juan County", "San Miguel County", "Sedgwick County", "Summit County", "Teller County", "Washington County", "Weld County", "Yuma County"],
    "Connecticut": ["Fairfield County", "Hartford County", "New Haven County", "Litchfield County", "Middlesex County", "New London County", "Tolland County", "Windham County"],
    "Delaware": ["New Castle County", "Kent County", "Sussex County"],
    "Florida": ["Miami-Dade County", "Broward County", "Hillsborough County", "Orange County", "Alachua County", "Baker County", "Bay County", "Bradford County", "Brevard County", "Calhoun County", "Charlotte County", "Citrus County", "Clay County", "Collier County", "Columbia County", "DeSoto County", "Dixie County", "Duval County", "Escambia County", "Flagler County", "Franklin County", "Gadsden County", "Gilchrist County", "Glades County", "Gulf County", "Hamilton County", "Hardee County", "Hendry County", "Hernando County", "Highlands County", "Holmes County", "Indian River County", "Jackson County", "Jefferson County", "Lafayette County", "Lake County", "Lee County", "Leon County", "Levy County", "Liberty County", "Madison County", "Manatee County", "Marion County", "Martin County", "Monroe County", "Nassau County", "Okaloosa County", "Okeechobee County", "Osceola County", "Palm Beach County", "Pasco County", "Pinellas County", "Polk County", "Putnam County", "St. Johns County", "St. Lucie County", "Santa Rosa County", "Sarasota County", "Seminole County", "Sumter County", "Suwannee County", "Taylor County", "Union County", "Volusia County", "Wakulla County", "Walton County", "Washington County"],
    "Georgia": ["Fulton County", "Cobb County", "DeKalb County", "Gwinnett County", "Appling County", "Atkinson County", "Bacon County", "Baker County", "Baldwin County", "Banks County", "Barrow County", "Bartow County", "Ben Hill County", "Berrien County", "Bibb County", "Bleckley County", "Brantley County", "Brooks County", "Bryan County", "Bulloch County", "Burke County", "Butts County", "Calhoun County", "Camden County", "Candler County", "Carroll County", "Catoosa County", "Charlton County", "Chatham County", "Chattahoochee County", "Chattooga County", "Cherokee County", "Clarke County", "Clay County", "Clayton County", "Clinch County", "Coffee County", "Colquitt County", "Columbia County", "Cook County", "Coweta County", "Crawford County", "Crisp County", "Dade County", "Dawson County", "Decatur County", "Dodge County", "Dooly County", "Dougherty County", "Douglas County", "Early County", "Echols County", "Effingham County", "Elbert County", "Emanuel County", "Evans County", "Fannin County", "Fayette County", "Floyd County", "Forsyth County", "Franklin County", "Gilmer County", "Glascock County", "Glynn County", "Gordon County", "Grady County", "Greene County", "Habersham County", "Hall County", "Hancock County", "Haralson County", "Harris County", "Hart County", "Heard County", "Henry County", "Houston County", "Irwin County", "Jackson County", "Jasper County", "Jeff Davis County", "Jefferson County", "Jenkins County", "Johnson County", "Jones County", "Lamar County", "Lanier County", "Laurens County", "Lee County", "Liberty County", "Lincoln County", "Long County", "Lowndes County", "Lumpkin County", "Macon County", "Madison County", "Marion County", "McDuffie County", "McIntosh County", "Meriwether County", "Miller County", "Mitchell County", "Monroe County", "Montgomery County", "Morgan County", "Murray County", "Muscogee County", "Newton County", "Oconee County", "Oglethorpe County", "Paulding County", "Peach County", "Pickens County", "Pierce County", "Pike County", "Polk County", "Pulaski County", "Putnam County", "Quitman County", "Rabun County", "Randolph County", "Richmond County", "Rockdale County", "Schley County", "Screven County", "Seminole County", "Spalding County", "Stephens County", "Stewart County", "Sumter County", "Talbot County", "Taliaferro County", "Tattnall County", "Taylor County", "Telfair County", "Terrell County", "Thomas County", "Tift County", "Toombs County", "Towns County", "Treutlen County", "Troup County", "Turner County", "Twiggs County", "Union County", "Upson County", "Walker County", "Walton County", "Ware County", "Warren County", "Washington County", "Wayne County", "Webster County", "Wheeler County", "White County", "Whitfield County", "Wilcox County", "Wilkes County", "Wilkinson County", "Worth County"],
    "Hawaii": ["Honolulu County", "Maui County", "Hawaii County", "Kalawao County", "Kauai County"],
    "Idaho": ["Ada County", "Canyon County", "Kootenai County", "Adams County", "Bannock County", "Bear Lake County", "Benewah County", "Bingham County", "Blaine County", "Boise County", "Bonner County", "Bonneville County", "Boundary County", "Butte County", "Camas County", "Caribou County", "Cassia County", "Clark County", "Clearwater County", "Custer County", "Elmore County", "Franklin County", "Fremont County", "Gem County", "Gooding County", "Idaho County", "Jefferson County", "Jerome County", "Latah County", "Lemhi County", "Lewis County", "Lincoln County", "Madison County", "Minidoka County", "Nez Perce County", "Oneida County", "Owyhee County", "Payette County", "Power County", "Shoshone County", "Teton County", "Twin Falls County", "Valley County", "Washington County"],
    "Illinois": ["Cook County", "DuPage County", "Lake County", "Adams County", "Alexander County", "Bond County", "Boone County", "Brown County", "Bureau County", "Calhoun County", "Carroll County", "Cass County", "Champaign County", "Christian County", "Clark County", "Clay County", "Clinton County", "Coles County", "Crawford County", "Cumberland County", "DeKalb County", "DeWitt County", "Douglas County", "Edgar County", "Edwards County", "Effingham County", "Fayette County", "Ford County", "Franklin County", "Fulton County", "Gallatin County", "Greene County", "Grundy County", "Hamilton County", "Hancock County", "Hardin County", "Henderson County", "Henry County", "Iroquois County", "Jackson County", "Jasper County", "Jefferson County", "Jersey County", "Jo Daviess County", "Johnson County", "Kane County", "Kankakee County", "Kendall County", "Knox County", "LaSalle County", "Lawrence County", "Lee County", "Livingston County", "Logan County", "Macon County", "Macoupin County", "Madison County", "Marion County", "Marshall County", "Mason County", "Massac County", "McDonough County", "McHenry County", "McLean County", "Menard County", "Mercer County", "Monroe County", "Montgomery County", "Morgan County", "Moultrie County", "Ogle County", "Peoria County", "Perry County", "Piatt County", "Pike County", "Pope County", "Pulaski County", "Putnam County", "Randolph County", "Richland County", "Rock Island County", "St. Clair County", "Saline County", "Sangamon County", "Schuyler County", "Scott County", "Shelby County", "Stark County", "Stephenson County", "Tazewell County", "Union County", "Vermilion County", "Wabash County", "Warren County", "Washington County", "Wayne County", "White County", "Whiteside County", "Will County", "Williamson County", "Winnebago County", "Woodford County"],
    "Indiana": ["Marion County", "Lake County", "Allen County", "Adams County", "Bartholomew County", "Benton County", "Blackford County", "Boone County", "Brown County", "Carroll County", "Cass County", "Clark County", "Clay County", "Clinton County", "Crawford County", "Daviess County", "Dearborn County", "Decatur County", "DeKalb County", "Delaware County", "Dubois County", "Elkhart County", "Fayette County", "Floyd County", "Fountain County", "Franklin County", "Fulton County", "Gibson County", "Grant County", "Greene County", "Hamilton County", "Hancock County", "Harrison County", "Hendricks County", "Henry County", "Howard County", "Huntington County", "Jackson County", "Jasper County", "Jay County", "Jefferson County", "Jennings County", "Johnson County", "Knox County", "Kosciusko County", "LaGrange County", "LaPorte County", "Lawrence County", "Madison County", "Marshall County", "Martin County", "Miami County", "Monroe County", "Montgomery County", "Morgan County", "Newton County", "Noble County", "Ohio County", "Orange County", "Owen County", "Parke County", "Perry County", "Pike County", "Porter County", "Posey County", "Pulaski County", "Putnam County", "Randolph County", "Ripley County", "Rush County", "St. Joseph County", "Scott County", "Shelby County", "Spencer County", "Starke County", "Steuben County", "Sullivan County", "Switzerland County", "Tippecanoe County", "Tipton County", "Union County", "Vanderburgh County", "Vermillion County", "Vigo County", "Wabash County", "Warren County", "Warrick County", "Washington County", "Wayne County", "Wells County", "White County", "Whitley County"],
    "Iowa": ["Polk County", "Linn County", "Scott County", "Adair County", "Adams County", "Allamakee County", "Appanoose County", "Audubon County", "Benton County", "Black Hawk County", "Boone County", "Bremer County", "Buchanan County", "Buena Vista County", "Butler County", "Calhoun County", "Carroll County", "Cass County", "Cedar County", "Cerro Gordo County", "Cherokee County", "Chickasaw County", "Clarke County", "Clay County", "Clayton County", "Clinton County", "Crawford County", "Dallas County", "Davis County", "Decatur County", "Delaware County", "Des Moines County", "Dickinson County", "Dubuque County", "Emmet County", "Fayette County", "Floyd County", "Franklin County", "Fremont County", "Greene County", "Grundy County", "Guthrie County", "Hamilton County", "Hancock County", "Hardin County", "Harrison County", "Henry County", "Howard County", "Humboldt County", "Ida County", "Iowa County", "Jackson County", "Jasper County", "Jefferson County", "Johnson County", "Jones County", "Keokuk County", "Kossuth County", "Lee County", "Louisa County", "Lucas County", "Lyon County", "Madison County", "Mahaska County", "Marion County", "Marshall County", "Mills County", "Mitchell County", "Monona County", "Monroe County", "Montgomery County", "Muscatine County", "O'Brien County", "Osceola County", "Page County", "Palo Alto County", "Plymouth County", "Pocahontas County", "Pottawattamie County", "Poweshiek County", "Ringgold County", "Sac County", "Shelby County", "Sioux County", "Story County", "Tama County", "Taylor County", "Union County", "Van Buren County", "Wapello County", "Warren County", "Washington County", "Wayne County", "Webster County", "Winnebago County", "Winneshiek County", "Woodbury County", "Worth County", "Wright County"],
    "Kansas": ["Johnson County", "Sedgwick County", "Wyandotte County", "Allen County", "Anderson County", "Atchison County", "Barber County", "Barton County", "Bourbon County", "Brown County", "Butler County", "Chase County", "Chautauqua County", "Cherokee County", "Cheyenne County", "Clark County", "Clay County", "Cloud County", "Coffey County", "Comanche County", "Cowley County", "Crawford County", "Decatur County", "Dickinson County", "Doniphan County", "Douglas County", "Edwards County", "Elk County", "Ellis County", "Ellsworth County", "Finney County", "Ford County", "Franklin County", "Geary County", "Gove County", "Graham County", "Grant County", "Gray County", "Greeley County", "Greenwood County", "Hamilton County", "Harper County", "Harvey County", "Haskell County", "Hodgeman County", "Jackson County", "Jefferson County", "Jewell County", "Kearny County", "Kingman County", "Kiowa County", "Labette County", "Lane County", "Leavenworth County", "Lincoln County", "Linn County", "Logan County", "Lyon County", "McPherson County", "Marion County", "Marshall County", "Meade County", "Miami County", "Mitchell County", "Montgomery County", "Morris County", "Morton County", "Nemaha County", "Neosho County", "Ness County", "Norton County", "Osage County", "Osborne County", "Ottawa County", "Pawnee County", "Phillips County", "Pottawatomie County", "Pratt County", "Rawlins County", "Reno County", "Republic County", "Rice County", "Riley County", "Rooks County", "Rush County", "Russell County", "Saline County", "Scott County", "Seward County", "Shawnee County", "Sheridan County", "Sherman County", "Smith County", "Stafford County", "Stanton County", "Stevens County", "Sumner County", "Thomas County", "Trego County", "Wabaunsee County", "Wallace County", "Washington County", "Wichita County", "Wilson County", "Woodson County"],
    "Kentucky": ["Jefferson County", "Fayette County", "Kenton County", "Adair County", "Allen County", "Anderson County", "Ballard County", "Barren County", "Bath County", "Bell County", "Boone County", "Bourbon County", "Boyd County", "Boyle County", "Bracken County", "Breathitt County", "Breckinridge County", "Bullitt County", "Butler County", "Caldwell County", "Calloway County", "Campbell County", "Carlisle County", "Carroll County", "Carter County", "Casey County", "Christian County", "Clark County", "Clay County", "Clinton County", "Crittenden County", "Cumberland County", "Daviess County", "Edmonson County", "Elliott County", "Estill County", "Fleming County", "Floyd County", "Franklin County", "Fulton County", "Gallatin County", "Garrard County", "Grant County", "Graves County", "Grayson County", "Green County", "Greenup County", "Hancock County", "Hardin County", "Harlan County", "Harrison County", "Hart County", "Henderson County", "Henry County", "Hickman County", "Hopkins County", "Jackson County", "Jessamine County", "Johnson County", "Knott County", "Knox County", "LaRue County", "Laurel County",  "Lawrence County", "Lee County", "Leslie County", "Letcher County", "Lewis County", "Lincoln County", "Livingston County", "Logan County", "Lyon County", "Madison County", "Magoffin County", "Marion County", "Marshall County", "Martin County", "Mason County", "McCracken County", "McCreary County", "McLean County", "Meade County", "Menifee County", "Mercer County", "Metcalfe County", "Monroe County", "Montgomery County", "Morgan County", "Muhlenberg County", "Nelson County", "Nicholas County", "Ohio County", "Oldham County", "Owen County", "Owsley County", "Pendleton County", "Perry County", "Pike County", "Powell County", "Pulaski County", "Robertson County", "Rockcastle County", "Rowan County", "Russell County", "Scott County", "Shelby County", "Simpson County", "Spencer County", "Taylor County", "Todd County", "Trigg County", "Trimble County", "Union County", "Warren County", "Washington County", "Wayne County", "Webster County", "Whitley County", "Wolfe County", "Woodford County"],
    "Louisiana": ["Orleans Parish", "Jefferson Parish", "East Baton Rouge Parish", "Acadia Parish", "Allen Parish", "Ascension Parish", "Assumption Parish", "Avoyelles Parish", "Beauregard Parish", "Bienville Parish", "Bossier Parish", "Caddo Parish", "Calcasieu Parish", "Caldwell Parish", "Cameron Parish", "Catahoula Parish", "Claiborne Parish", "Concordia Parish", "DeSoto Parish", "East Carroll Parish", "East Feliciana Parish", "Evangeline Parish", "Franklin Parish", "Grant Parish", "Iberia Parish", "Iberville Parish", "Jackson Parish", "Jefferson Davis Parish", "La Salle Parish", "Lafayette Parish", "Lafourche Parish", "Lincoln Parish", "Livingston Parish", "Madison Parish", "Morehouse Parish", "Natchitoches Parish", "Ouachita Parish", "Plaquemines Parish", "Pointe Coupee Parish", "Rapides Parish", "Red River Parish", "Richland Parish", "Sabine Parish", "St. Bernard Parish", "St. Charles Parish", "St. Helena Parish", "St. James Parish", "St. John the Baptist Parish", "St. Landry Parish", "St. Martin Parish", "St. Mary Parish", "St. Tammany Parish", "Tangipahoa Parish", "Tensas Parish", "Terrebonne Parish", "Union Parish", "Vermilion Parish", "Vernon Parish", "Washington Parish", "Webster Parish", "West Baton Rouge Parish", "West Carroll Parish", "West Feliciana Parish", "Winn Parish"],
    "Maine": ["Cumberland County", "York County", "Penobscot County", "Androscoggin County", "Aroostook County", "Franklin County", "Hancock County", "Kennebec County", "Knox County", "Lincoln County", "Oxford County", "Piscataquis County", "Sagadahoc County", "Somerset County", "Waldo County", "Washington County"],
    "Maryland": ["Baltimore County", "Montgomery County", "Prince George’s County"],
    "Massachusetts": ["Middlesex County", "Suffolk County", "Worcester County"],
    "Michigan": ["Wayne County", "Oakland County", "Macomb County"],
    "Minnesota": ["Hennepin County", "Ramsey County", "Dakota County"],
    "Mississippi": ["Hinds County", "Harrison County", "DeSoto County"],
    "Missouri": ["St. Louis County", "Jackson County", "Greene County"],
    "Montana": ["Yellowstone County", "Gallatin County", "Missoula County"],
    "Nebraska": ["Douglas County", "Lancaster County", "Sarpy County"],
    "Nevada": ["Clark County", "Washoe County", "Carson City"],
    "New Hampshire": ["Hillsborough County", "Rockingham County", "Merrimack County"],
    "New Jersey": ["Bergen County", "Middlesex County", "Essex County"],
    "New Mexico": ["Bernalillo County", "Doña Ana County", "Santa Fe County"],
    "New York": ["New York County", "Kings County", "Queens County", "Erie County", "Monroe County"],
    "North Carolina": ["Mecklenburg County", "Wake County", "Guilford County"],
    "North Dakota": ["Cass County", "Burleigh County", "Grand Forks County"],
    "Ohio": ["Cuyahoga County", "Franklin County", "Hamilton County"],
    "Oklahoma": ["Oklahoma County", "Tulsa County", "Cleveland County"],
    "Oregon": ["Multnomah County", "Washington County", "Lane County"],
    "Pennsylvania": ["Philadelphia County", "Allegheny County", "Montgomery County"],
    "Rhode Island": ["Providence County", "Kent County", "Washington County"],
    "South Carolina": ["Charleston County", "Greenville County", "Richland County"],
    "South Dakota": ["Minnehaha County", "Pennington County", "Lincoln County"],
    "Tennessee": ["Shelby County", "Davidson County", "Knox County"],
    "Texas": ["Harris County", "Dallas County", "Tarrant County", "Bexar County", "Travis County"],
    "Utah": ["Salt Lake County", "Utah County", "Davis County"],
    "Vermont": ["Chittenden County", "Rutland County", "Washington County"],
    "Virginia": ["Fairfax County", "Prince William County", "Loudoun County", "Clarke County"],
    "Washington": ["King County", "Pierce County", "Snohomish County", "Adams County", "Asotin County", "Benton County", "Chelan Count", "Clallam County", "Clark County", "Columbia County", "Cowlitz County", "Douglas County", "Ferry County", "Franklin County", "Garfield County", "Grant County", "Grays Harbor County", "Island County", "Jefferson County", "Kitsap County", "Kittitas County", "Klickitat County", "Lewis County", "Lincoln County", "Mason County", "Okanogan County", "Pacific County", "Pend Oreille County", "San Juan County", "Skagit County", "Skamania County", "Spokane County", "Stevens County", "Thurston County", "Wahkiakum County", "Walla Walla County", "Whatcom County", "Whitman County", "Yakima County"],
    "West Virginia": ["Kanawha County", "Berkeley County", "Monongalia County", "Jefferson County", "Barbour County", "Boone County", "Braxton County", "Brooke County", "Cabell County", "Calhoun County", "Clay County", "Doddridge County", "Fayette County", "Gilmer County", "Grant County", "Greenbrier County", "Hampshire County", "Hancock County", "Hardy County", "Harrison County", "Jackson County", "Lewis County", "Lincoln County", "Logan County", "McDowell County", "Marion County", "Marshall County", "Mason County", "Mercer County", "Mineral County", "Mingo County", "Monroe County", "Morgan County", "Nicholas County", "Ohio County", "Pendleton County", "Pleasants County", "Pocahontas County", "Preston County", "Putnam County", "Raleigh County", "Randolph County", "Ritchie County", "Roane County", "Summers County", "Taylor County", "Tucker County", "Tyler County", "Upshur County", "Wayne County", "Webster County", "Wetzel County", "Wirt County", "Wood County", "Wyoming County"],
    "Wisconsin": ["Milwaukee County", "Dane County", "Waukesha County", "Adams County", "Ashland County", "Barron County", "Bayfield County", "Brown County", "Buffalo County", "Burnett County", "Calumet County", "Chippewa County", "Clark County", "Columbia County", "Crawford County", "Dodge County", "Door County", "Douglas County", "Dunn County", "Eau Claire County", "Florence County", "Fond du Lac County", "Forest County", "Grant County", "Green County", "Green Lake County", "Iowa County", "Iron County", "Jackson County", "Jefferson County", "Juneau County", "Kenosha County", "Kewaunee County", "La Crosse County", "Lafayette County", "Langlade County", "Lincoln County", "Manitowoc County", "Marathon County", "Marinette County", "Marquette County", "Menominee County", "Monroe County", "Oconto County", "Oneida County", "Outagamie County", "Ozaukee County", "Pepin County", "Pierce County", "Polk County", "Portage County", "Price County", "Racine County", "Richland County", "Rock County", "Rusk County", "St. Croix County", "Sauk County", "Sawyer County", "Shawano County", "Sheboygan County", "Taylor County", "Trempealeau County", "Vernon County", "Vilas County", "Walworth County", "Washburn County", "Washington County", "Waupaca County", "Waushara County", "Winnebago County", "Wood County"],
    "Wyoming": ["Laramie County", "Natrona County", "Sweetwater County", "Albany County", "Big Horn County", "Campbell County", "Carbon County", "Converse County", "Crook County", "Fremont County", "Goshen County", "Hot Springs County", "Johnson County", "Lincoln County", "Niobrara County", "Park County", "Platte County", "Sheridan County", "Sublette County", "Teton County", "Uinta County", "Washakie County", "Weston County"],
    "District of Columbia": ["Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5", "Ward 6", "Ward 7", "Ward 8"]         
        },
        "Canada": {
    "Alberta": ["Calgary", "Edmonton", "Red Deer"],
    "British Columbia": ["Vancouver", "Victoria", "Kelowna", "Prince George"],
    "Manitoba": ["Winnipeg", "Brandon", "Steinbach"],
    "New Brunswick": ["Fredericton", "Saint John", "Moncton"],
    "Newfoundland and Labrador": ["St. John's", "Corner Brook", "Gander"],
    "Nova Scotia": ["Halifax", "Sydney", "Truro"],
    "Ontario": ["Toronto", "Ottawa", "Hamilton", "London"],
    "Prince Edward Island": ["Charlottetown", "Summerside"],
    "Quebec": ["Montreal", "Quebec City", "Sherbrooke", "Gatineau"],
    "Saskatchewan": ["Saskatoon", "Regina", "Prince Albert"],
    "Northwest Territories": ["Yellowknife", "Inuvik"],
    "Nunavut": ["Iqaluit", "Rankin Inlet"],
    "Yukon": ["Whitehorse", "Dawson City"]
    },
        "Mexico": {
    "Aguascalientes": ["Aguascalientes City", "Jesús María", "Calvillo"],
    "Baja California": ["Tijuana", "Mexicali", "Ensenada"],
    "Baja California Sur": ["La Paz", "Los Cabos", "Comondú"],
    "Campeche": ["Campeche City", "Ciudad del Carmen"],
    "Chiapas": ["Tuxtla Gutiérrez", "San Cristóbal de las Casas", "Tapachula"],
    "Chihuahua": ["Chihuahua City", "Ciudad Juárez", "Delicias"],
    "Coahuila": ["Saltillo", "Torreón", "Piedras Negras"],
    "Colima": ["Colima City", "Manzanillo", "Tecomán"],
    "Durango": ["Durango City", "Gómez Palacio", "Lerdo"],
    "Guanajuato": ["León", "Irapuato", "Celaya", "Guanajuato City"],
    "Guerrero": ["Acapulco", "Chilpancingo", "Iguala"],
    "Hidalgo": ["Pachuca", "Tula de Allende", "Tulancingo"],
    "Jalisco": ["Guadalajara", "Puerto Vallarta", "Zapopan", "Tepatitlán"],
    "Mexico City": ["Álvaro Obregón", "Iztapalapa", "Benito Juárez", "Coyoacán"],
    "Mexico State": ["Toluca", "Naucalpan", "Ecatepec"],
    "Michoacán": ["Morelia", "Uruapan", "Lázaro Cárdenas"],
    "Morelos": ["Cuernavaca", "Temixco", "Jiutepec"],
    "Nayarit": ["Tepic", "Bahía de Banderas", "Compostela"],
    "Nuevo León": ["Monterrey", "Guadalupe", "San Nicolás de los Garza"],
    "Oaxaca": ["Oaxaca de Juárez", "Salina Cruz", "Juchitán"],
    "Puebla": ["Puebla City", "Tehuacán", "Atlixco"],
    "Querétaro": ["Querétaro City", "San Juan del Río", "El Marqués"],
    "Quintana Roo": ["Cancún", "Chetumal", "Playa del Carmen", "Tulum"],
    "San Luis Potosí": ["San Luis Potosí City", "Soledad", "Ciudad Valles"],
    "Sinaloa": ["Culiacán", "Mazatlán", "Los Mochis"],
    "Sonora": ["Hermosillo", "Ciudad Obregón", "Nogales"],
    "Tabasco": ["Villahermosa", "Cárdenas", "Comalcalco"],
    "Tamaulipas": ["Reynosa", "Matamoros", "Tampico"],
    "Tlaxcala": ["Tlaxcala City", "Apizaco", "Huamantla"],
    "Veracruz": ["Veracruz City", "Xalapa", "Coatzacoalcos", "Poza Rica"],
    "Yucatán": ["Mérida", "Valladolid", "Tizimín"],
    "Zacatecas": ["Zacatecas City", "Guadalupe", "Fresnillo"]
        }
    },
    "South America": {
        "Brazil": {
            "São Paulo": ["São Paulo City", "Campinas"],
            "Rio de Janeiro": ["Rio de Janeiro City", "Niterói"]
        },
        "Argentina": {
            "Buenos Aires": ["Buenos Aires City", "La Plata"],
            "Córdoba": ["Córdoba City", "Villa Carlos Paz"]
        },
        "Chile": {
            "Santiago Metropolitan": ["Santiago", "Puente Alto"],
            "Valparaíso": ["Valparaíso", "Viña del Mar"]
        }
    },
    "Europe": {
        "United Kingdom": {
            "England": ["London", "Manchester"],
            "Scotland": ["Edinburgh", "Glasgow"],
            "Wales": ["Cardiff", "Swansea"]
        },
        "France": {
            "Île-de-France": ["Paris", "Versailles"],
            "Provence-Alpes-Côte d'Azur": ["Marseille", "Nice"]
        },
        "Germany": {
            "Bavaria": ["Munich", "Nuremberg"],
            "North Rhine-Westphalia": ["Cologne", "Düsseldorf"]
        },
        "Italy": {
            "Lazio": ["Rome", "Viterbo"],
            "Lombardy": ["Milan", "Bergamo"]
        }
    },
    "Africa": {
        "Nigeria": {
            "Lagos": ["Lagos Mainland", "Ikeja"],
            "Kano": ["Kano City", "Gwale"]
        },
        "Kenya": {
            "Nairobi": ["Westlands", "Kasarani"],
            "Mombasa": ["Mvita", "Changamwe"]
        },
        "South Africa": {
            "Gauteng": ["Johannesburg", "Pretoria"],
            "Western Cape": ["Cape Town", "Stellenbosch"]
        },
        "Egypt": {
            "Cairo Governorate": ["Cairo", "Helwan"],
            "Alexandria": ["Alexandria City", "Montaza"]
        }
    },
    "Asia": {
        "India": {
            "Maharashtra": ["Mumbai", "Pune"],
            "Tamil Nadu": ["Chennai", "Madurai"],
            "West Bengal": ["Kolkata", "Howrah"]
        },
        "China": {
            "Guangdong": ["Guangzhou", "Shenzhen"],
            "Beijing": ["Dongcheng", "Haidian"]
        },
        "Japan": {
            "Tokyo": ["Chiyoda", "Shinjuku"],
            "Osaka": ["Kita", "Naniwa"]
        },
        "Philippines": {
            "Metro Manila": ["Quezon City", "Manila"],
            "Cebu": ["Cebu City", "Mandaue"]
        },
        "Gaza Strip": {
            "North Gaza Governorate": ["Jabalia", "Beit Hanoun", "Beit Lahia", "Umm al-Nasr"]
        }
    },
    "Oceania": {
        "Australia": {
            "New South Wales": ["Sydney", "Newcastle"],
            "Victoria": ["Melbourne", "Geelong"],
            "Queensland": ["Brisbane", "Cairns"]
        },
        "New Zealand": {
            "Auckland Region": ["Auckland City", "Manukau"],
            "Canterbury": ["Christchurch", "Ashburton"]
        },
        "Fiji": {
            "Central Division": ["Suva", "Nausori"],
            "Western Division": ["Lautoka", "Nadi"]
        }
    },
    "Antarctica": {
        "Research Stations": {
            "Ross Ice Shelf": ["McMurdo Station", "Scott Base", "Mawson Station", "Davis Station", "Amundsen–Scott South Pole Station"],
            "Queen Maud Land": ["Troll Station", "Neumayer Station III", "Wasa", "Svea", "Princess Elisabeth Antarctica", "Kohnen", "Maitri", "SANAE IV", "Novolazarevskaya", "Nordenskiöld Base"],
            "Antarctic Peninsula": ["Frei Base", "Palmer Station", "Rothera Research Station", "Vernadsky Research Base"]
        }
    }
}

# 🌊 Flood tier logic
def determine_tier(probability):
    if probability > 0.75:
        return "RED"
    elif probability > 0.45:
        return "AMBER"
    else:
        return "GREEN"

def generate_forecast():
    data = {"forecasts": {}, "timestamp": datetime.utcnow().isoformat() + "Z"}

    for continent, countries in REGION_STRUCTURE.items():
        data["forecasts"][continent] = {}
        for country, states in countries.items():
            data["forecasts"][continent][country] = {}
            for state, counties in states.items():
                data["forecasts"][continent][country][state] = {}
                for county in counties:
                    p_val = round(random.uniform(0.05, 0.95), 2)
                    tier = determine_tier(p_val)
                    data["forecasts"][continent][country][state][county] = {
                        "P_final": p_val,
                        "tier": tier
                    }

    return data


if __name__ == "__main__":
    forecast_data = generate_forecast()
    output_path = "data/outputs/all_forecasts.json"

    with open(output_path, "w") as f:
        json.dump(forecast_data, f, indent=2)

    print("✅ Forecast generation complete:", forecast_data["timestamp"])
