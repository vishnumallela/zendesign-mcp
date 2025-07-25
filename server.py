import asyncio
import requests
from fastmcp import FastMCP
from typing import Dict, Any
import json
import os
mcp = FastMCP("Oraczen-Zendesign-MCP")



@mcp.tool
def get_component_info(component_name: str) -> Dict[str, Any]:
    """
    Get component information from the Zendesign design system.
    
    Args:
        component_name: The name of the component (e.g., 'button', 'card', 'input')
    
    Returns:
        Dict containing component schema, dependencies, files, and styling information
    """
    try:
        url = f"https://zendesign-psi.vercel.app/r/{component_name}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        component_data = response.json()
        
        # Extract key information for easier consumption
        result = {
            "name": component_data.get("name", component_name),
            "title": component_data.get("title", ""),
            "description": component_data.get("description", ""),
            "type": component_data.get("type", ""),
            "dependencies": component_data.get("dependencies", []),
            "files": component_data.get("files", []),
            "cssVars": component_data.get("cssVars", {}),
            "raw_data": component_data
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch component '{component_name}': {str(e)}",
            "available_hint": "Make sure the component name is correct (e.g., 'button', 'card', 'input')"
        }
    except Exception as e:
        return {
            "error": f"Error processing component data: {str(e)}"
        }

@mcp.tool
def get_llms_text() -> Dict[str, str]:
    """
    Get the llms.txt content from Zendesign for full design system context.this includes overall design system context, component information, and other relevant information.
    
    Returns:
        Dict containing the llms.txt content and metadata
    """
    try:
        url = "https://zendesign-psi.vercel.app/llms.txt"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        content = response.text
        
        return {
            "content": content,
            "source": url,
            "status": "success",
            "length": len(content),
            "description": "Full design system context and guidelines from Zendesign"
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch llms.txt: {str(e)}",
            "content": "",
            "status": "error"
        }
    except Exception as e:
        return {
            "error": f"Error processing llms.txt: {str(e)}",
            "content": "",
            "status": "error"
        }
    

@mcp.tool
def get_avaialble_components() -> Dict[str, str]:
    """
    this will give you the list of all components that are avaialble in the design system
    """
    try:
        url = "https://zendesign-psi.vercel.app/r/registry.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        components = [item["name"] for item in data["items"]]
        return {
            "components": components,
            "status": "success",
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch components: {str(e)}",
            "status": "error"
        }
    except Exception as e:
        return {
            "error": f"Error processing components: {str(e)}",
            "components": [],
            "status": "error"
        }
    
@mcp.tool
def get_component_code(component_name: str) -> Dict[str, str]:
    """returns the content code of the component.this includes the component code, the component css, and the component js"""
    try:
        url = f"https://zendesign-psi.vercel.app/r/e/{component_name}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        files_content = {}
        for file in data["files"]:
            files_content[file["name"]] = file["content"]
        return {
            "content": json.dumps(files_content,indent=4),
            "status": "success",
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to fetch component code: {str(e)}",
            "status": "error"
        }
    except Exception as e:
        return {
            "error": f"Error processing component code: {str(e)}",
            "status": "error"
        }
    
    
    
if __name__ == "__main__":
    port = int(os.getenv("PORT", 9000))
    mcp.run(transport="sse", port=port)
