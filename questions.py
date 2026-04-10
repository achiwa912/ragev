questions_keywords = [
    {
        "id": "q01",
        "query": "What does PREV stand for and what is its purpose?",
        "keywords": ["Plan", "Verify", "self-criticism"],
        "expected_answer": "PREV stands for Plan, Reason, Execute and Verify. Its purpose is to address the LLM weakness of jumping into conclusions too early by forcing the LLM to slow down and verify its output."
    },
    {
        "id": "q02",
        "query": "What does ReAct stand for and what loop does it use?",
        "keywords": ["Reason-Action", "Thought", "Observation"],
        "expected_answer": "ReAct stands for Reason-Action. It is a micro-pattern that breaks a step into a Thought, Action, Observation loop."
    },
    {
        "id": "q03",
        "query": "What is the difference between HITL and HOTL?",
        "keywords": ["Human-in-the-loop", "Human-on-the-loop", "checkpoint"],
        "expected_answer": "Human-in-the-loop (HITL) means the pipeline stops until a human approves, while Human-on-the-loop (HOTL) means the pipeline continues but logs state so that a human can check or audit it later."
    },
    {
        "id": "q04",
        "query": "What are two reasons why LLMs perform poorly on long prompts?",
        "keywords": ["mistakes accumulate", "U-shaped attention", "middle"],
        "expected_answer": "Two reasons are: (1) mistakes are not corrected when made so they accumulate and wrongly change the context, and (2) LLMs have a U-shaped attention span, meaning sentences in the middle of documents may not receive the attention they deserve."
    },
    {
        "id": "q05",
        "query": "What is the scratch pad effect in synthesis patterns?",
        "keywords": ["intermediate outputs", "hallucinations", "thinking state"],
        "expected_answer": "The scratch pad effect refers to displaying intermediate outputs at each stage so the LLM can manage its thinking state — its output acts as its input. Without this, if the template says give me the final answer only, the LLM might lose track and produce hallucinations."
    },
    {
        "id": "q06",
        "query": "What mini PC did the author buy for their homelab and how much did it cost?",
        "keywords": ["AceMagic", "N150", "$200"],
        "expected_answer": "The author bought AceMagic's mini PC for less than $200. It has an Intel N150 processor, 16GB DDR4 RAM and 1TB S-ATA SSD."
    },
    {
        "id": "q07",
        "query": "What hypervisor is running on the homelab server and why was it chosen?",
        "keywords": ["Proxmox", "snapshot", "open source"],
        "expected_answer": "Proxmox 8.4.0 is running as the hypervisor. It was chosen for its snapshot and backup features, and because it is open source, unlike VMware which the author no longer trusts."
    },
    {
        "id": "q08",
        "query": "What is Caddy and what killer feature does it have?",
        "keywords": ["reverse proxy", "certificate", "Let's Encrypt"],
        "expected_answer": "Caddy is a web server and reverse proxy. Its killer feature is automatic certificate deployment and renewal — it automatically acquires certificates from Let's Encrypt, removing the burden of manual cert renewal for server admins."
    },
    {
        "id": "q09",
        "query": "What is Immich and what AI features does it have?",
        "keywords": ["Google Photos", "face-recognition", "searching photos"],
        "expected_answer": "Immich is a Google Photos alternative that syncs photos and videos directly from mobile devices to a server. It has AI features including face recognition and searching photos with words."
    },
    {
        "id": "q10",
        "query": "What is Pi-hole and how was it deployed on the homelab?",
        "keywords": ["DNS", "ad-blocker", "CT"],
        "expected_answer": "Pi-hole is a DNS with network-wide ad-blocking. It was deployed as a CT (container) directly on Proxmox, rather than inside the Ubuntu VM, so that it could be used from the Ubuntu VM on the homelab PC."
    },
    {
        "id": "q11",
        "query": "What is DDNS and which tool did the author use for it?",
        "keywords": ["dynamic IP", "porkbun-ddns", "domain name"],
        "expected_answer": "DDNS (Dynamic DNS) is a service that automatically updates the IP address for a domain name when the IP address changes. The author used porkbun-ddns, a DDNS service specifically designed for domain names purchased from Porkbun, deployed via docker-compose."
    },
    {
        "id": "q12",
        "query": "What is RomM and why is it lightweight on the server?",
        "keywords": ["ROM manager", "EmulatorJS", "browser"],
        "expected_answer": "RomM is a ROM manager for retro games. It uses a JavaScript port of the RetroArch emulator that runs in browsers, which means the server itself does very little processing, making it very lightweight."
    },
    {
        "id": "q13",
        "query": "What is vocaBull and what three practice modes does it offer?",
        "keywords": ["flashcard", "definition to word", "type words"],
        "expected_answer": "vocaBull is a flashcard web application for vocabulary building. It offers three modes: (1) Flashcard word to definition, (2) Flashcard definition to word, and (3) Type words from the definitions."
    },
    {
        "id": "q14",
        "query": "What is the Shifting Learning Window method in vocaBull?",
        "keywords": ["learning window", "10 words", "memorized"],
        "expected_answer": "The Shifting Learning Window method maintains a learning window of 10 words that the user is actively working on. As a word is memorized, it is replaced by a new word from the word book, causing the window to shift through the book. This combines high-frequency repetitions of a small number of words with low-frequency repetitions across the full book."
    },
    {
        "id": "q15",
        "query": "What happens when you click 'knew it!' in vocaBull flashcard practice?",
        "keywords": ["skip", "score", "five rounds"],
        "expected_answer": "Clicking 'knew it!' increases the word's score by 5, meaning the user will not see that word for 5 rounds."
    },
    {
        "id": "q16",
        "query": "What format is required for loading words from a file in vocaBull?",
        "keywords": ["tab", "definition", "sample sentence"],
        "expected_answer": "Each line must contain a word, a definition, and an optional sample sentence, all separated by tabs. The format is: word, tab, definition, optionally tab, sample sentence."
    },
    {
        "id": "q17",
        "query": "What does the vocaBull Export all feature save and what format does it use?",
        "keywords": ["books", "scores", "JSON"],
        "expected_answer": "The Export all feature exports all books, all words in them, and scores to a JSON file named vocabull.json."
    },
    {
        "id": "q18",
        "query": "Why did the author choose to install Ubuntu rather than Rocky Linux for the homelab VM, and what network configuration did they apply to it?",
        "keywords": ["RedHat", "apt", "fixed IP"],
        "expected_answer": "The author has more experience with RedHat Linux and uses Rocky Linux at work, but decided to install Ubuntu for the homelab. They note the two are not very different and they are simply not yet used to apt. They assigned a fixed IP address to the VM since it is a server."
    },
    {
        "id": "q19",
        "query": "Why are PREV, ReAct, and Self-Ask considered different patterns even though all three address LLMs jumping to conclusions, and can they be combined?",
        "keywords": ["self-criticism", "knowledge gaps", "logic gaps"],
        "expected_answer": "They address different weaknesses: PREV fixes lack of self-criticism by forcing the LLM to verify what it did; ReAct fixes knowledge gaps by retrieving new information and reflecting it in later steps; Self-Ask fixes logic gaps by adding structure to reasoning. They are different and can even be combined for reasonably complex tasks."
    },
    {
        "id": "q20",
        "query": "What malware concern existed with the AceMagic mini PC, and how did the author address it, and what OS did they replace it with?",
        "keywords": ["malware", "initialize", "Proxmox"],
        "expected_answer": "AceMagic once had malware in its PCs. The author was not concerned because they intended to initialize the entire storage from the beginning, wiping the pre-installed Windows 11. They then installed Proxmox 8.4.0 as the hypervisor."
    }
]
