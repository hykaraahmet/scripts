#!/usr/bin/env python3
import sys
import random
import string

# Expanded word list for password generation
words = [
    "cat", "dog", "bird", "fish", "sun", "moon", "star", "tree", "sky", "hill",
    "lake", "wind", "cloud", "rain", "snow", "meow", "bark", "growl", "peak", "valley",
    "river", "stone", "forest", "desert", "ocean", "breeze", "flame", "shadow", "light", "dream",
    "castle", "meadow", "ridge", "canyon", "storm", "thunder", "lightning", "whisper", "echo", "frost",
    "glacier", "tundra", "prairie", "savanna", "jungle", "mountain", "volcano", "horizon", "twilight", "dawn",
    "everest", "denali", "ararat", "anatolia", "siberia", "mediterranean", "egypt", "japan", "mogadishu",
    "berlin", "ankara", "washington", "london", "moscow", "istanbul", "amazon", "sahara", "wildcat",
    "cyber", "crystal", "donkey", "galaxy", "supernova", "orange", "summit", "victory", "heaven", "havana",
    "equator", "salvation", "dragon", "swordfish", "spearfish", "trinity", "noisycrow", "sydney", "seagull",
    "shortzebra", "stickyrabbit", "butterfly", "smartfox", "rustybat", "fishbowl", "firstlove", "seconddate",
    "firstkiss", "exwife", "stockbroker", "sailboat", "flatwave", "smirkingwhale", "sleepingmonkey", "ant",
    "callmemaybe", "mediumrare", "beatmeifyoucan", "turkishbath", "greeksalad", "ottomanslap", "magicbox",
    "blinddate", "livelongandprosper", "itsajerseything", "iwasthinking", "showmeyours", "guesswhatimthinking",
    "musictomyears", "helpmetohelpyou", "thatsallshewrote", "heartbreak", "calculus", "maytheforcebewithyou",
    "etphonehome", "bondjamesbond", "showmethemoney", "youcanthandlethetruth", "illhavewhatsheshaving",
    "youregonnaneedabiggerboat", "illbeback", "iseedeadpeople", "houstonwehaveaproblem", "youhadmeathello",
    "greedisgood", "sayhellotomylittlefriend", "hastalavistababy", "myprecious", "snapoutofit", "thisisnotadrill",
    "chinatown", "ghostinthemachine", "forpetessake", "jesushchrist", "koshersalt", "battlecat", "luckynumber",
    "washmachine", "tinglecherry", "smackburger", "firstrejection", "missedthebus", "purpleeye", "statistically",
    "angrykaren", "moopoint", "hiddenstash", "fronttothepast", "drunkworks", "maze", "sweet", "fantasy",
    "icon", "voodoo", "onepingonly", "speed", "swimfan", "sexywhisper", "shelikesme", "napkindrawing",
    "jupiter", "lostyournumber", "freshair", "callhertonight", "takeabreak", "lifeisshort", "magneticfield",
    "blackhole", "neutronstar", "eventhorizon", "singularity", "spirits", "youarenotalone", "yummy",
    "jarhead", "banana", "hazelnut", "giant", "banker", "honeypot", "wallstreet", "moneywell", "relax",
    "judge", "reward", "freedom", "independence", "liberty", "cheekybastard", "iwannaseethemanager",
    "clickbait", "cursor", "negotiate", "ilovemyjob", "corneroffice", "trophywife", "mercurial", "coalmine",
    "patio", "firesale", "cashflow", "balancesheet", "income", "equity", "budget", "credit", "investment",
    "profit", "skeletoncloset", "diversification", "revenue", "coinsurance", "collateral", "interest",
    "cosigner", "demand", "donate", "entrepreneur", "exchange", "federal", "financial", "wealth",
    "treasure", "grace", "handsome", "inflation", "liquidity", "mobile", "overdraft", "payroll",
    "paycheck", "policy", "premium", "pinewood", "streamline", "celebrity", "pacific", "atlantic",
    "party", "comedy", "dominance", "queen", "nightwish", "carryon", "persist", "cashisking",
    "shadowsense", "slide", "slick", "government", "consume", "likely", "blessyourheart", "storytime",
    "triangle", "miracle", "friends", "statue", "blamegame", "reasonable", "vanilla", "humanity",
    "atmosphere", "gooddeal", "okayboy", "alientech", "deadofwinter", "rollout", "walkingaround",
    "jump", "sparetire", "sniper", "screwdriver", "medschool", "disasterrelief", "allegedly", "meltdown",
    "followtheline", "reload", "shakedown", "serialnumber", "grandfather", "century", "halfandhalf",
    "highlight", "underline", "emphasize", "membersonly", "marina", "blueskies", "framebyframe",
    "spectrum", "machinelearning", "blacklight", "variable", "flush", "inthatcase", "opposite",
    "turningpoint", "apex", "weird", "drone", "ufo", "obviously", "youcanonlyimagine", "lastthing",
    "scenario", "fallguy", "goforit", "readysetgo", "material", "diamond", "heist", "coincidence",
    "whynot", "bigbang", "heat", "sparkplug", "mainsail", "timeout", "rockingchair", "unclesam",
    "distortion", "greeneyes", "fake", "inconclusion", "release", "focus", "optical", "valhalla",
    "claim", "defense", "information", "balance", "intelligence", "artificial", "king", "commando",
    "scuba", "submarine", "relativity", "occupation", "masterful", "helicopter", "surgeon",
    "applepie", "blacksea", "africa", "corporate", "methodical", "deserve", "blamegame", "entity",
    "fortherecord", "justkidding", "suspicious", "meteor", "difference", "heavy", "propaganda",
    "spy", "specifically", "confirmed", "convince", "aggressive", "intervention", "angel", "politics",
    "nomeansno", "white", "takeaseat", "boomerang", "venus", "annual", "progress", "annoy", "action",
    "fundamental", "foundation", "quantum", "interaction", "regain", "theory", "measure", "tiny",
    "string", "philosophical", "consistent", "story", "experiment", "cosmos", "observation", "massive",
    "particle", "however", "field", "energy", "know", "microwave", "solid", "postulate", "modify",
    "difficult", "dealwithit", "tellmemore", "rotate", "distribute", "therefore", "watertight",
    "slowly", "linked", "chain", "immune", "constant", "recently", "possible", "shift", "alert",
    "place", "origin", "dimension", "question", "forever", "science", "razor", "simplicity",
    "religion", "tribute", "ritual", "physics", "impossible", "everything", "standard", "patterns",
    "symmetry", "whatsoever", "insummary", "remain", "inspire", "candle", "candy", "cannedbeans",
    "mountainair", "forestflower", "nuclearoption", "thermonuclear", "unlock", "explore", "remember",
    "heroic", "stronghold", "bluepine", "rainyday", "hypnotize", "power", "factory", "engineer",
    "critical", "subscribe", "everyone", "race", "generation", "cheaper", "frontier", "deploy",
    "scale", "bigger", "imagine", "jetfuel", "solarpower", "stable", "density", "neighborhood",
    "rechargeable", "essential", "frustrated", "countdown", "liftoff", "inheritance", "criticism",
    "respect", "next", "platter", "standup", "fightback", "uplifting", "brother", "infinitely",
    "equally", "veteran", "trumpet", "guitar", "storm", "hurricane", "dinosaur", "neutral",
    "dueprocess", "economy"
]

# Special characters for passwords
special_chars = "!@#$%^&*+-=?"

def generate_password(length):
    if length < 4:  # Minimum length to ensure complexity
        raise ValueError("Password length must be at least 4 characters")
    
    # Choose number of words based on length
    if length < 8:
        num_words = 1
    elif length < 16:
        num_words = random.randint(1, 2)
    else:
        num_words = random.randint(2, 4)  # Use 2-4 words for longer passwords
    
    # Select words and ensure they don't exceed length minus separators and one number
    selected_words = []
    total_word_length = 0
    attempts = 0
    max_attempts = 10
    
    while attempts < max_attempts:
        selected_words = random.sample(words, num_words)
        total_word_length = sum(len(word) for word in selected_words)
        # Reserve space for up to 2 special chars per boundary and one number
        if total_word_length <= length - 2 * (num_words - 1) - 1:
            break
        num_words = max(1, num_words - 1)  # Try fewer words if too long
        attempts += 1
    
    # If still too long, use a single short word
    if total_word_length > length - 2 * (num_words - 1) - 1:
        selected_words = [random.choice([w for w in words if len(w) <= length - 2])]
        num_words = 1
        total_word_length = len(selected_words[0])
    
    # Capitalize some words randomly for variety
    for i in range(len(selected_words)):
        if random.choice([True, False]):
            selected_words[i] = selected_words[i].capitalize()
    
    # Build password with 1-2 special characters between words
    password_parts = []
    for i, word in enumerate(selected_words):
        password_parts.append(word)
        if i < len(selected_words) - 1:  # Add 1-2 special chars between words
            num_special = random.randint(1, 2) if length >= 16 else 1
            password_parts.append("".join(random.choice(special_chars) for _ in range(num_special)))
    
    # Combine parts
    password = "".join(password_parts)
    
    # Add one number (required)
    password += random.choice(string.digits)
    
    # Fill remaining length with letters (prefer letters to reduce complexity)
    current_length = len(password)
    remaining_length = length - current_length
    for _ in range(max(0, remaining_length)):
        password += random.choice(string.ascii_letters)
    
    # Shuffle only the non-word parts to keep words intact
    if remaining_length > 0 or num_words > 1:
        word_positions = []
        current_pos = 0
        for part in password_parts:
            word_positions.append((current_pos, current_pos + len(part)))
            current_pos += len(part)
        
        # Extract non-word characters (special chars and filler)
        non_word_chars = list(password[current_pos:])
        random.shuffle(non_word_chars)
        
        # Rebuild password, preserving word positions
        final_password = []
        current_pos = 0
        non_word_index = 0
        for start, end in word_positions:
            # Add characters before the word
            while current_pos < start and non_word_index < len(non_word_chars):
                final_password.append(non_word_chars[non_word_index])
                non_word_index += 1
                current_pos += 1
            # Add the word
            final_password.append(password[start:end])
            current_pos = end
        # Add remaining non-word characters
        final_password.extend(non_word_chars[non_word_index:])
        password = "".join(final_password)
    
    # Trim to desired length
    return password[:length]

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: ./Randomize.py <length>")
        sys.exit(1)
    
    try:
        length = int(sys.argv[1])
    except ValueError:
        print("Error: Length must be an integer")
        sys.exit(1)
    
    # Generate and print 20 passwords with numbering
    for i in range(1, 21):
        try:
            password = generate_password(length)
            print(f"{i}. {password}")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
    