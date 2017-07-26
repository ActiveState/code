proc read_socket {sock} {
set pdu [read $sock]
if {[catch {binary scan $pdu ccc d(disver) d(exercise) d(kind)}]} {return}

switch -- $d(kind) {
 1	{
	# ENTITY STATE
	catch {binary scan $pdu ccccISSSSSccccSccccccSccccIIIWWWIIIIcA39cA11I \
	d(disver) d(exercise) d(kind) d(family) d(time) d(length) pad \
	d(site) d(host) d(ent) d(force) d(art) \
	d(kind) d(domain) d(country) d(cat) d(subcat) d(spec) d(extra) \
	d(altkind) d(altdomain) d(altcountry) d(altcat) d(altsubcat) d(altspec) d(altextra) \
	d(velx) d(vely) d(velz) d(locx) d(locy) d(locz) d(orientx) d(orienty) d(orientz) \
	d(appearance) d(dra) pad d(charset) d(marking) d(cap)} result

	}
 2	{
	# FIRE
	catch {binary scan $pdu ccccISSSSSSSSSSSSSSIWWWccSccccSSSSIIII \
	d(disver) d(exercise) d(kind) d(family) d(time) d(length) 0 \
	d(site) d(host) d(ent) d(sitetgt) d(hosttgt) d(enttgt) \
	d(sitemun) d(hostmun) d(entmun) d(siteevt) d(hostevt) d(entevt) \
	d(mission) d(locx) d(locy) d(locz) \
	d(kind) d(domain) d(country) d(cat) d(subcat) d(spec) d(extra) \
	d(warhead) d(fuze) d(quantity) d(rate) d(velx) d(vely) d(velz) d(range)} result

	}
 3	{
	# DETONATION
	catch {binary scan $pdu ccccISSSSSSSSSSSSSSIIIWWWccSccccSSSSIIIccS \
	d(disver) d(exercise) d(kind) d(family) d(time) d(length) 0 \
	d(site) d(host) d(ent) d(sitetgt) d(hosttgt) d(enttgt) \
	d(sitemun) d(hostmun) d(entmun) d(siteevt) d(hostevt) d(entevt) \
	d(velx) d(vely) d(velz) d(locx) d(locy) d(locz) \
	d(kind) d(domain) d(country) d(cat) d(subcat) d(spec) d(extra) \
	d(warhead) d(fuze) d(quantity) d(rate) d(entx) d(enty) d(entz) d(result) \
	d(parts) d(art)} result

	}
}

}
