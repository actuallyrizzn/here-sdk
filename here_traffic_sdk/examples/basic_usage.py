"""
Basic usage examples for HERE Traffic SDK
"""

from here_traffic_sdk import (
    HereTrafficClient,
    LocationReference,
    GeospatialFilter,
    AuthMethod
)

# Example 1: Using API Key authentication
def example_api_key():
    """Example using API key authentication"""
    client = HereTrafficClient(api_key="YOUR_API_KEY")
    
    # Get traffic flow for London (1km radius)
    flow_response = client.v7.get_flow_circle(
        latitude=51.50643,
        longitude=-0.12719,
        radius_meters=1000,
        location_referencing=LocationReference.SHAPE
    )
    
    print(f"Found {len(flow_response.flows)} flow segments")
    print(f"Free flow speeds: {flow_response.free_flow_speeds[:5]}")
    
    # Get traffic incidents
    incidents_response = client.v7.get_incidents_circle(
        latitude=51.50643,
        longitude=-0.12719,
        radius_meters=1000
    )
    
    print(f"Found {incidents_response.incident_count} incidents")
    print(f"Critical incidents: {len(incidents_response.get_critical_incidents())}")


# Example 2: Using OAuth authentication
def example_oauth():
    """Example using OAuth 2.0 authentication"""
    client = HereTrafficClient(
        access_key_id="YOUR_ACCESS_KEY_ID",
        access_key_secret="YOUR_ACCESS_KEY_SECRET",
        auth_method=AuthMethod.OAUTH
    )
    
    # Use the same API
    response = client.v7.get_flow_bbox(
        lat1=51.5,
        lon1=-0.13,
        lat2=51.51,
        lon2=-0.12
    )
    
    print(f"Flow data: {response.flows}")


# Example 3: Using custom geospatial filters
def example_custom_filter():
    """Example using custom geospatial filters"""
    client = HereTrafficClient(api_key="YOUR_API_KEY")
    
    # Create a custom circle filter
    filter_str = GeospatialFilter.circle(51.50643, -0.12719, 2000)
    
    response = client.v7.get_flow(
        location_referencing=LocationReference.SHAPE,
        geospatial_filter=filter_str
    )
    
    print(f"Flow response: {response.data}")


# Example 4: Using bounding box
def example_bbox():
    """Example using bounding box"""
    client = HereTrafficClient(api_key="YOUR_API_KEY")
    
    # Get flow data for a bounding box
    flow_response = client.v7.get_flow_bbox(
        lat1=51.5,
        lon1=-0.13,
        lat2=51.51,
        lon2=-0.12
    )
    
    # Get incidents for the same area
    incidents_response = client.v7.get_incidents_bbox(
        lat1=51.5,
        lon1=-0.13,
        lat2=51.51,
        lon2=-0.12
    )
    
    print(f"Flow segments: {len(flow_response.flows)}")
    print(f"Incidents: {incidents_response.incident_count}")


# Example 5: Check API availability
def example_availability():
    """Example checking API availability"""
    client = HereTrafficClient(api_key="YOUR_API_KEY")
    
    availability = client.v7.get_availability()
    
    if availability.available:
        print("API is available")
        print(f"Coverage areas: {len(availability.coverage_areas)}")
    else:
        print("API is not available")


# Example 6: Using legacy v6.3 API
def example_v6():
    """Example using legacy v6.3 API"""
    client = HereTrafficClient(api_key="YOUR_API_KEY")
    
    # Use v6.3 API
    response = client.v6.get_flow_bbox(
        lat1=51.5,
        lon1=-0.13,
        lat2=51.51,
        lon2=-0.12
    )
    
    print(f"v6.3 Flow data: {response.flows}")


if __name__ == "__main__":
    print("HERE Traffic SDK Examples")
    print("=" * 50)
    print("\nNote: Replace 'YOUR_API_KEY' with your actual API key")
    print("or use OAuth credentials for authentication.\n")

