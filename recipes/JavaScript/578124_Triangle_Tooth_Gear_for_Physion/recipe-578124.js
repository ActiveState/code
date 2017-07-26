//Triangle_Tooth_Gear.script
function Triangle_Tooth_Gear(x,y,radius,tooth_size,tooth_count){
	phi=0;
	phi_plus=360.0/tooth_count;
	phi_plus=(2*3.1415926*phi_plus)/360;
	tooth=0;
	radius2=radius-tooth_size;
	var gear = new QPolygonF();
	for(tooth=0;tooth<tooth_count;tooth++){
		px=radius*Math.cos(phi);
		py=radius*Math.sin(phi);
		gear.append(new QPointF(x+px,y+py));
		
		px=radius2*Math.cos(phi+(phi_plus/2));
		py=radius2*Math.sin(phi+(phi_plus/2));
		gear.append(new QPointF(x+px,y+py));
		
		phi=phi+phi_plus;
	}
	return world.createPolygon(gear);
}
