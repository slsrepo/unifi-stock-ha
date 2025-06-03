# UniFi Stock Check

A Home Assistant custom integration that monitors Ubiquiti UniFi product availability. It uses the Shopify JSON API (when available) and falls back to HTML scraping to detect when a product is back in stock.

## Installation via [HACS](https://hacs.xyz) (Recommended)

1. **Add Custom Repository**  
   - In Home Assistant, go to **Settings → Devices & Services → HACS**.  
   - Click the three-dot menu (⋮) → **Custom repositories**.  
   - Set **Repository type** to `Integration` and **URL** to `https://github.com/slsrepo/unifi-stock-ha`.  
   - Click **Add**.
  <p dir="auto"><a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=slsrepo&amp;repository=unifi-stock-ha&amp;category=integration" rel="nofollow"><img src="https://camo.githubusercontent.com/8cec5af6ba93659beb5352741334ef3bbee70c4cb725f20832a1b897dfb8fc5f/68747470733a2f2f6d792e686f6d652d617373697374616e742e696f2f6261646765732f686163735f7265706f7369746f72792e737667" alt="Open your Home Assistant instance and open a repository inside the Home Assistant Community Store." data-canonical-src="https://my.home-assistant.io/badges/hacs_repository.svg" style="max-width: 100%;"></a></p>

2. **Install the Integration**  
   - In HACS, go to **Integrations** and search for **UniFi Stock Check**.  
   - Click **Install**.  
   - Restart Home Assistant when prompted.
  <p dir="auto"><a href="https://my.home-assistant.io/redirect/config_flow_start/?domain=sl_unifi_stock" rel="nofollow"><img src="https://camo.githubusercontent.com/adbb09f7a40eb3933f3220dfe49dd8dff1e0f86acf59e9803662bb6f8f988910/68747470733a2f2f6d792e686f6d652d617373697374616e742e696f2f6261646765732f636f6e6669675f666c6f775f73746172742e737667" alt="Open your Home Assistant instance and start setting up a new integration." data-canonical-src="https://my.home-assistant.io/badges/config_flow_start.svg" style="max-width: 100%;"></a></p>

3. **Verify**  
   - After Home Assistant restarts, go to **Settings → Devices & Services**.
   - You should see **UniFi Stock Check** among the integrations.
<p dir="auto"><a href="https://my.home-assistant.io/redirect/integration/?domain=sl_unifi_stock" rel="nofollow"><img src="https://camo.githubusercontent.com/15a86d08f7563387040afaf0ccbc46e4bee0f1002dfba800b01196693feff43f/68747470733a2f2f6d792e686f6d652d617373697374616e742e696f2f6261646765732f696e746567726174696f6e2e737667" alt="Open your Home Assistant instance and show an integration." data-canonical-src="https://my.home-assistant.io/badges/integration.svg" style="max-width: 100%;"></a></p>

## Manual Installation (Alternative)

1. Copy the entire `sl_unifi_stock/` folder into your Home Assistant `custom_components/` directory.
2. Restart Home Assistant.
3. Go to **Settings → Devices & Services → + Add Integration** and select **UniFi Stock Check**.

## Configuration

1. Go to **Settings → Devices & Services → + Add Integration**.  
2. Search for **UniFi Stock Check** and click to add.  
3. Fill in the form:  
   - **Product URL**: Required. Must include `/products/` (e.g. `https://store.ui.com/collections/unifi-network/products/unifi-switch-lite-8-poe`).  
   - **Region**: us, eu, uk, ca (default: `us`).  
   - **Name**: Product name (default: “UniFi Stock”).

After clicking Submit, a new sensor entity is created (slugified from the name) and it begins polling automatically (at 30 seconds intervals).

## Using the Sensor

- Sensor entity IDs look like `sensor.<slugified_name>`, for example `sensor.unifi_switch_lite_8_poe`.  
- **States**:  
  - **In Stock**  
  - **Out of Stock**  
  - **Unavailable** (if both API and scraping fail)  

Use these sensors in automations, dashboards, or notifications.

## Example Automation

```yaml
automation:
  - alias: "Get a notification when UCG-Fiber is back in stock"
    trigger:
      - platform: state
        entity_id: sensor.ucg_fiber
        to: "In Stock"
    action:
      - service: notify.notify
        data:
          title: "UniFi Stock Alert"
          message: "The UCG-Fiber is now in stock!"
```

---

© All Rights Reserved, [Sl's Repository Ltd](https://slsrepo.com/), 2025.
