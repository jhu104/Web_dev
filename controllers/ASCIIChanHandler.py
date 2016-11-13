from controllers.BaseHandler import BaseHandler
from google.appengine.ext import db
from models.Art import Art
import urllib2
from xml.dom import minidom

IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except:
        return

    parsed = minidom.parseString(content)
    coordsDOM = parsed.getElementsByTagName("gml:coordinates")
    
    if len(coordsDOM):
        coords = coordsDOM[0].firstChild.nodeValue
        lon, lat = coords.split(',')
    return db.GeoPt(lat, lon)

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmaps_img(points):
    points_url = "&".join("markers="+str(point[0])+","+str(point[1]) for point in points)
    return GMAPS_URL+points_url

class ASCIIChanHandler(BaseHandler):
    

    def render_front(self, title="",art="",error=""):
        arts = db.GqlQuery("SELECT * FROM Art ORDER BY created DESC LIMIT 10")
        #prevents the running of multiple queries
        arts = list(arts)

        points = []
        for art in arts:
            if art.coords:
                points.append(art.coords)
        
        img_url = None
        if points:
            img_url = gmaps_img(points)

        self.render("asciichan.html",title=title,art=art,error=error,arts=arts, img_url=img_url)

    def get(self):
        self.render_front()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        
        if title and art:
            coords = get_coords(self.request.remote_addr)
            art = Art(title=title, art=art)
            if coords:
                art.coords = coords
            art.put()
            
            self.redirect("/asciichan")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(title, art, error)
