  var S='stroke="currentColor" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"';
  var ICON={
    steak:'<path class="f3" '+S+' d="M12 30c0-10 10-16 22-16s18 8 18 16-8 18-20 18S12 40 12 30z"/><ellipse class="f2" '+S+' cx="40" cy="28" rx="5" ry="4"/>',
    chicken:'<path class="f1" '+S+' d="M22 14c10-4 22 4 20 16-1 7-8 11-14 10l-8 8a4 4 0 1 1-5-5l2-2a4 4 0 1 1 4-5l1-1c-4-6-6-17 0-21z"/>',
    sausage:'<path class="f3" '+S+' d="M14 40c6-14 20-24 34-26 4 0 6 4 3 7-10 4-20 12-28 24-3 4-11 1-9-5z"/>',
    fish:'<path class="f4" '+S+' d="M10 32c8-10 20-12 30-6l12-8v28l-12-8c-10 6-22 4-30-6z"/><circle cx="22" cy="30" r="2" fill="currentColor"/>',
    dairy:'<path class="f2" '+S+' d="M22 10h20v8l6 8v28H16V26l6-8z"/><path class="f4" '+S+' d="M16 34h32v10H16z"/>',
    butter:'<path class="f1" '+S+' d="M10 28l22-10 22 10v14L32 52 10 42z"/><path '+S+' fill="none" d="M10 28l22 10 22-10M32 38v14"/>',
    cola:'<path class="f3" '+S+' d="M27 8h10v8c6 4 7 8 7 14v24a4 4 0 0 1-4 4H24a4 4 0 0 1-4-4V30c0-6 1-10 7-14z"/><path class="f2" '+S+' d="M20 32h24v10H20z"/>',
    beer:'<path class="f1" '+S+' d="M16 18h26v34a4 4 0 0 1-4 4H20a4 4 0 0 1-4-4z"/><path class="f2" '+S+' d="M14 18a6 6 0 0 1 8-8 7 7 0 0 1 12 0 6 6 0 0 1 10 8z"/><path '+S+' fill="none" d="M42 26h6a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4h-6"/>',
    wine:'<path class="f3" '+S+' d="M28 8h8v12c5 3 7 7 7 12v20a4 4 0 0 1-4 4H25a4 4 0 0 1-4-4V32c0-5 2-9 7-12z"/>',
    coffee:'<path class="f2" '+S+' d="M14 24h30v16a12 12 0 0 1-12 12h-6a12 12 0 0 1-12-12z"/><path '+S+' fill="none" d="M44 28h4a5 5 0 0 1 0 10h-5M22 10c-2 4 2 6 0 10M30 10c-2 4 2 6 0 10"/>',
    choc:'<path class="f3" '+S+' d="M14 12h36v40H14z"/><path '+S+' fill="none" d="M14 25h36M14 38h36M26 12v40M38 12v40"/>',
    sweets:'<circle class="f1" '+S+' cx="32" cy="32" r="12"/><path class="f3" '+S+' d="M20 32l-10-8v16zM44 32l10-8v16z"/>',
    chips:'<path class="f1" '+S+' d="M20 12h24v40H20z"/><ellipse class="f2" '+S+' cx="32" cy="12" rx="12" ry="4"/><path '+S+' fill="none" d="M20 26h24M20 40h24"/>',
    apple:'<path class="f3" '+S+' d="M32 20c-6-5-18-3-18 10 0 12 8 22 14 22 2 0 3-1 4-1s2 1 4 1c6 0 14-10 14-22 0-13-12-15-18-10z"/><path '+S+' fill="none" d="M32 20c0-6 2-9 6-11"/>',
    veg:'<path class="f1" '+S+' d="M44 18L16 50c-2 2-5-1-3-3l23-33c4-4 10 0 8 4z"/><path class="f4" '+S+' d="M44 18c2-6 6-8 10-8-1 4-3 8-10 8zM44 18c6-2 10 0 12 3-4 1-9 1-12-3z"/>',
    potato:'<path class="f1" '+S+' d="M14 34c0-10 8-18 20-18s16 6 16 14-6 18-20 18c-10 0-16-6-16-14z"/><circle cx="26" cy="30" r="1.6" fill="currentColor"/><circle cx="38" cy="36" r="1.6" fill="currentColor"/>',
    pizza:'<path class="f1" '+S+' d="M32 52L12 16c12-6 28-6 40 0z"/><circle class="f3" cx="28" cy="24" r="3"/><circle class="f3" cx="38" cy="30" r="3"/><circle class="f3" cx="31" cy="38" r="2.5"/>',
    grain:'<path class="f2" '+S+' d="M18 16h28l-2 8 4 28H16l4-28z"/><path '+S+' fill="none" d="M20 24h24"/>',
    clean:'<path class="f4" '+S+' d="M22 26h20v26H22z"/><path class="f2" '+S+' d="M26 14h10l2 12H24zM36 16h10"/>',
    tool:'<path class="f2" '+S+' d="M12 40h40v10H12zM18 40V22h28v18"/><path '+S+' fill="none" d="M24 30h16"/>',
    battery:'<path class="f1" '+S+' d="M22 14h20v40H22z"/><path '+S+' fill="currentColor" d="M28 8h8v6h-8z"/><path class="f3" d="M24 40h16v12H24z"/>',
    star:'<path class="f1" '+S+' d="M32 8l7 15 16 2-12 11 3 16-14-8-14 8 3-16L9 25l16-2z"/>',
    shirt:'<path class="f4" '+S+' d="M22 10l-12 8 5 10 5-3v29h24V25l5 3 5-10-12-8c-2 4-6 6-10 6s-8-2-10-6z"/>',
    paw:'<circle class="f1" '+S+' cx="20" cy="26" r="5"/><circle class="f1" '+S+' cx="44" cy="26" r="5"/><circle class="f1" '+S+' cx="27" cy="16" r="5"/><circle class="f1" '+S+' cx="37" cy="16" r="5"/><path class="f1" '+S+' d="M32 30c-8 0-14 10-12 16 2 6 8 4 12 4s10 2 12-4c2-6-4-16-12-16z"/>',
    plant:'<path class="f3" '+S+' d="M20 38h24l-3 16H23z"/><path class="f4" '+S+' d="M32 38c0-12-6-20-14-22 0 10 6 18 14 22zM32 38c0-10 6-16 14-18 0 8-6 16-14 18z"/>',
    toy:'<path class="f1" '+S+' d="M12 30h20v20H12z"/><path class="f4" '+S+' d="M32 30h20v20H32z"/><path class="f3" '+S+' d="M22 10h20v20H22z"/>',
    bag:'<path class="f1" '+S+' d="M14 22h36l-4 32H18z"/><path '+S+' fill="none" d="M24 22v-4a8 8 0 0 1 16 0v4"/>'
  };
  var RULES=[
    [/hähnchen|chicken|wings|pute|geflügel-brat|nugget/i,'chicken'],
    [/wurst|wiener|salami|schinken|aufschnitt/i,'sausage'],
    [/hack|steak|roulade|gulasch|bifteki|nacken|klopse|fleisch/i,'steak'],
    [/fisch|thunfisch|lachs|scholle/i,'fish'],
    [/butter/i,'butter'],
    [/käse|buko|philadelphia|joghurt|milch|pudding|milchreis|sahne|grünländer|mozzarella|drink/i,'dairy'],
    [/cola|fanta|sprite|red bull|energy|barista|hafer/i,'cola'],
    [/bier|pils|radler|urquell/i,'beer'],
    [/sekt|wein|merlot|bourbon|jim beam|amarula/i,'wine'],
    [/kaffee|jacobs|nescaf|lavazza/i,'coffee'],
    [/schokolade|milka|twix|nestlé minis|celebrations|favourites|m&m/i,'choc'],
    [/fruchtgummi|trolli|knoppers|eis\b|mövenpick eis|süß/i,'sweets'],
    [/pringles|chips|cashew|nuss/i,'chips'],
    [/äpfel|apfel|banane|zitrone|clementine|obst/i,'apple'],
    [/kartoffel|pommes/i,'potato'],
    [/möhren|gurke|tomate|kürbis|champignon|rotkohl|weißkraut|gemüse/i,'veg'],
    [/pizza/i,'pizza'],
    [/reis|zucker|nudel|kondensmilch|frühstück|konfitüre|sauce|fertiggericht/i,'grain'],
    [/batterie/i,'battery'],
    [/reiniger|ariel|citronensäure|waschmittel/i,'clean'],
    [/pfanne|stabmixer|schüssel|staubsauger|kaffeemaschine/i,'tool'],
    [/hoodie|pullover|hose|shirt|pyjama|stiefel/i,'shirt'],
    [/led|tanne|baum|flocke|stern/i,'star'],
    [/katze|hund|tier/i,'paw'],
    [/kaktus|pflanze|blume/i,'plant'],
    [/lupilu|holz-küche|spiel/i,'toy'],
    [/steppdecke|kissen|bettwäsche/i,'bag']
  ];
  var CATICON={'Fleisch & Wurst':'steak','Getränke':'cola','Süßes':'sweets','Haushalt':'clean','Deko':'star','Mode':'shirt','Tier':'paw','Pflanzen':'plant','Spielzeug':'toy'};
  function iconFor(i){
    for (var k=0;k<RULES.length;k++) if (RULES[k][0].test(i.name)) return ICON[RULES[k][1]];
    return ICON[CATICON[i.cat]] || ICON.bag;
  }
