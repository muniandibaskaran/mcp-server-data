from mcp.server.fastmcp import FastMCP
import pandas as pd
import os
import uvicorn

# Initialize FastMCP server
mcp = FastMCP("mcpDataExploration")

# Read a Ecommerce Sales data (CSV file)

base_dir = os.path.dirname(__file__)  # folder of this script
csv_path = os.path.join(base_dir, "online-ecommerce.csv")
# sales_df = pd.read_csv("/Users/muniandibaskaran/Desktop/learning/repo/mcp-server-data/ecommerce-mcp-server/online-ecommerce.csv")
sales_df = pd.read_csv(csv_path)

#get product details based on status
@mcp.tool()
async def get_product_status(status="processing"):
    """ Get product details based on status and order by order number to know priority"""
    return sales_df[sales_df["Status"].str.lower() == status.lower()].sort_values(by="Order_Number")

#get samsung sales details
@mcp.tool()
async def get_brand_sales(brand="samsung"):
    """ Get brand based sales details"""
    return sales_df[sales_df["Brand"].str.lower() == brand.lower()]["Total_Cost"].sum()

#get all sales details based on brands
@mcp.tool()
async def get_all_brands_sales():
    """ Get all sales details based on brands"""
    return sales_df.groupby("Brand")["Total_Cost"].sum()

#get Ajay Sharma sales details
@mcp.tool()
async def get_supervisor_sales(supervisor="ajay sharma"):
    """ Get Supervisor based sales details"""
    return sales_df[sales_df["Assigned Supervisor"].str.lower() == supervisor.lower()]["Total_Cost"].sum()

#get all sales details based on supervisor
@mcp.tool()
async def get_all_supervisor_sales():
    """ Get all Supervisor sales details"""
    return sales_df.groupby("Assigned Supervisor")["Total_Cost"].sum()

# ------------------------------
# Start FastMCP
# ------------------------------
if __name__ == "__main__":
    print("Started")
    uvicorn.run(mcp.sse_app(),host="0.0.0.0", port=8000)