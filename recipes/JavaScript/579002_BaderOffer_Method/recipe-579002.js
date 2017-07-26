// http://bechirot.gov.il/election/about/Pages/CalculatingSeatsMethod.aspx
// http://www.knesset.gov.il/lexicon/eng/seats_eng.htm
// http://main.knesset.gov.il/About/Lexicon/Pages/seats.aspx

/**
 * Computes the Badder-Offer score for specific party.
 *
 * @param {party_votes} Two columns, name-votes pairs.
 * @param {agreement_pairs} Two columns, name-name pairs.
 * @param {party} The name of the party to be shown.
 * @param {qualifying_threshold} אחוז החסימה.
 * @customfunction
 */
function BadderOfferMethod(party_votes, agreement_pairs, party, qualifying_threshold) {
  if (typeof qualifying_threshold === 'undefined')
     qualifying_threshold = 0.0325;
  var parties = prepare_data_(party_votes, agreement_pairs);
  var passed_parties = filter_parties_(parties, qualifying_threshold);
  var agreements_list = get_agreement_list_(passed_parties);
  mandate_splitting_(agreements_list).forEach(split_share_);
  var d = make_dict(parties);
  return d[party].seats;
}

function list_indicator_(x) {
  /* The reason for adding 1 is for determining what the indicator would be
  if the pair would receive that additional seat. */
  return Math.floor(x.votes / (x.seats + 1))
}

/*
 חלוקה ראשונה
 א. מחלקים את סה"כ הקולות הכשרים של הרשימות המשתתפות בחלוקת המנדטים ל-120 (מספר המקומות העומדים לחלוקה), והתוצאה היא המודד הכללי.
 ב. מחלקים את סה"כ הקולות של כל רשימה המשתתפת בחלוקה למודד הכללי ומקבלים את מספר המנדטים שקיבלה הרשימה.
 ג. בדרך זו, מחלקים את הקולות של כל הרשימות שעברו את אחוז החסימה ומשתתפות בחלוקה.
 ד. המספרים השלמים היוצאים מהחלוקה הם מספר המנדטים.
*/
function get_agreement_list_(passed_parties) {
  // first phase
  var total_votes = sum_(passed_parties, 'votes');
  var general_indicator = Math.floor(total_votes / 120);
  passed_parties.forEach(function(p) {
    p.agreement.seats += Math.floor(p.votes / general_indicator);
  });
  return passed_parties.map(key_('agreement')).toSet();
}
/*
חלוקה שניה
ה. מחברים את כל המנדטים, והמנדטים הנותרים עד להשלמת מספר המנדטים ל-120, אותם מחלקים על פי שיטת מודד הרשימה הגדול ביותר.
למשל, בבחירות לכנסת ה-18 נותרו 5 מנדטים לחלוקה.
ו. לצורך חלוקת המנדטים הנותרים, רואים 2 רשימות שהתקשרו ביניהן כרשימה אחת –מחברים את הקולות הכשרים שקיבלו 2 הרשימות ואת מספר המנדטים שקיבלו 2 הרשימות בחלוקה הראשונה, ומתייחסים אליהם בשלב זה כאל רשימת מועמדים אחת, זאת בתנאי שכל אחת מהרשימות עברה את אחוז החסימה.
ז. את המנדטים הנותרים מחלקים לפי מודד לכל רשימה לפי הנוסחה:
 
מודד רשימה     =     מספר הקולות שקיבלה הרשימה
  ________________________________________
לחלק ל     -     מספר המנדטים שקיבלה בחלוקה הראשונה + 1

קובעים כך על פי הנוסחה האמורה את המודד לכל רשימה. רשימה שלה המודד הגדול ביותר מקבלת את המנדט.
ח. לרשימה שקיבלה מנדט בחלוקת המקומות הנותרים נקבע מודד רשימה חדש בהתאם למספר המנדטים שיש לה.
ט. כך קובעים מודדים עד לחלוקת כל המנדטים הנותרים.

*/
function mandate_splitting_(agreements_list) {
  // second phase
  var seats_so_far = sum_(agreements_list, 'seats');
  agreements_list.forEach(function(s) { 
    s.votes = s.parties.sum('votes');
  });
  for (var i = seats_so_far; i < 120; i++) {
    agreements_list.max(list_indicator_).seats += 1;
  }
  return agreements_list
}

/*

3.	חלוקת המנדטים בין הרשימות הקשורות ביניהן
עתה נותר לקבוע איזו רשימה מבין שתי רשימות שהתקשרו ביניהן תקבל את המנדט הנוסף שבו זכו שתיהן בחלוקת המנדטים הנותרים.
קביעה זו נעשית גם היא בשני שלבים.
להלן שלבי החישוב:
שלב א'
א. קביעת מודד פנימי אחיד למנדט של זוג הרשימות המתקשרות.
מודד פנימי אחיד למנדט     =     מספר הקולות הכשרים של שתי הרשימות
  ________________________________________
לחלק ל     -     מספר המנדטים שקיבלו שתי הרשימות
 
ב. בודקים כמה מנדטים אמורה לקבל כל רשימה בנפרד על פי המודד הנ"ל.
היינו,
מספר המנדטים שקיבלה הרשימה בנפרד     =     סה"כ הקולות הכשרים שקיבלה רשימה בנפרד
  ________________________________________
לחלק ל     -                         מודד למנדט

שלב ב'
על פי מספר המנדטים שקיבלו שתי הרשימות ביחד, נותר מנדט נוסף לחלוקה.
את המנדט הנוסף תקבל רשימה שלה "מודד רשימה אישי הגדול ביותר".
חישוב המודד האישי לכל רשימה בנפרד נעשה באותה דרך חישוב של חלוקת המנדטים הנותרים.
היינו, לפי הנוסחה:
מודד רשימה     =     מספר הקולות הכשרים שקיבלה הרשימה בנפרד
  ________________________________________
לחלק ל     -     מספר המנדטים שקיבלה הרשימה בנפרד + 1
 
*/
function split_share_(s) {
  if (s.parties.length === 1) {
    s.parties[0].seats = s.seats;
    return;
  }
  // split between sharing parties
  var indicator = Math.floor(s.votes / s.seats);
  s.parties.forEach(function(p)  {
    p.seats = Math.floor(p.votes / indicator);
  });
  s.parties.max(list_indicator_).seats += 1;
}

/*
1. קביעת הרשימות המשתתפות בחלוקת המנדטים
 א. מסכמים את סך הקולות הכשרים שקיבלה כל אחת מרשימות המועמדים.
 ב. קובעים את מס' הקולות המהווה את אחוז החסימה.
אחוז החסימה = 3.25% מכלל הקולות הכשרים.
 ג. רשימות המועמדים שלא זכו במספר הקולות הדרוש – לא משתתפות בחלוקת המנדטים.
 ד. קובעים את מספר הקולות הכשרים של הרשימות המשתתפות בחלוקת המנדטים.
המספר הכולל של הקולות הכשרים של כל הרשימות פחות מספר הקולות הכשרים של רשימות שלא עברו את אחוז החסימה ולא משתתפות בחלוקה שווה לסה"כ הקולות הכשרים של הרשימות המשתתפות בחלוקת המנדטים.
*/
function filter_parties_(parties, qualifying_threshold_percentage) {
  var total_votes = parties.sum('votes');
  function passed(party) {
    return party.votes >= total_votes * qualifying_threshold_percentage;
  }
  var passed_parties = parties.filter(passed);
  passed_parties.forEach(function(p) {
    p.agreement.parties = p.agreement.parties.filter(passed);
  });
  return passed_parties;
}

function Agreement(parties) {
  return {
    seats: 0,
    parties: parties
  }
}

function Party(name, votes) {
  var res = {
    name: name,
    votes: votes,
    seats: 0
  };
  res.agreement = Agreement([res]);
  return res;
}

function prepare_data_(party_votes, agreement_pairs) {
  var parties = {}
  var all_parties = [];
  party_votes.forEach(function(nv) {
    var name = nv[0], votes = nv[1];
    parties[name] = Party(name, votes);
    all_parties.push(parties[name]);
  });
  agreement_pairs.forEach(function(pair) {
    var p1 = parties[pair[0]];
    var p2 = parties[pair[1]];
    p1.agreement = Agreement([p2, p1]);
    p2.agreement = p1.agreement;
  });
  return all_parties;
}




function make_dict(parties) {
  var res = {};
  parties.forEach(function(p) {
    res[p.name] = p;
  });
  return res;
}

function test() {
  var party_votes = [ 
  ['Likud',	925279],
  ['Labor',	455183],
  ['Shinui',	386535],
  ['Shas',	258879],
  ['Ichud Leumi-Yisrael Beiteinu',	173973],
  ['Meretz',	164122],
  ['United Torah Judaism',	135087],
  ['National Religious Party',	132370],
  ['Hadash',	93819],
  ['Am Ehad',	86808],
  ['Balad',	71299],
  ['Yisrael BeAliyah',	67719],
  ['United Arab List',	65551],
  ];
  var agreement_pairs = [  ];
  var res = BadderOfferMethod(party_votes, agreement_pairs, 'Likud');
  return 0;
}

//HELPERS

function key_(f) {
  if (typeof f == 'string')
     return function(p) { return p[f]; };
  if (typeof f == 'undefined')
    return function(x) { return x; };
  return f;
}

Array.prototype.max = function(key) {
  key = key_(key);
  return this.reduce(function(x, y) {
    return key(x) > key(y) ? x : y;
  });
};
Array.prototype.sum = function(key) {
  return sum_(this, key);
};
Array.prototype.toSet = function(key) {
  var res = [];
  this.forEach(function(p) {
      var val = key_(key)(p);
      if (res.indexOf(val) < 0)
          res.push(val);
  });
  return res;
}
Array.prototype.min = function() {
  return Math.min.apply(null, this);
};

function sum_(arr, key) {
  if (!arr.length)
    return 0;
  return arr.map(key_(key)).reduce(function(a, b) { return a + b });
}
