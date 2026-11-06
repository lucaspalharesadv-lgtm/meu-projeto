#!/bin/bash
# Runs until discovery ends: every 8 minutes merges domains and crawls the new ones; then processes and finalizes.
cd /tmp/claude-0/-home-user-meu-projeto/e6925dc5-ccb5-56d3-90f7-9e38f32b3a69/scratchpad/bulk
log(){ echo "$(date +%H:%M:%S) $*" >> orchestrate.log; }
log "início"
while true; do
  python3 -I domains_from_disc.py >> orchestrate.log 2>&1
  cat domains_INT.jsonl domains_BR.jsonl > domains_all.jsonl
  python3 -I crawl.py domains_all.jsonl v2 24 >> crawl_v2.log 2>&1
  log "crawl pass concluído: $(wc -l < crawl_v2.jsonl) domínios rastreados"
  if ! pgrep -f "discover.py" > /dev/null; then log "descoberta terminou"; break; fi
  sleep 480
done
python3 -I domains_from_disc.py >> orchestrate.log 2>&1
cat domains_INT.jsonl domains_BR.jsonl > domains_all.jsonl
python3 -I crawl.py domains_all.jsonl v2 24 >> crawl_v2.log 2>&1
log "crawl final: $(wc -l < crawl_v2.jsonl)"
python3 -I process_bulk.py crawl_v2.jsonl > process.log 2>&1
python3 -I finalize_bulk.py > finalize.log 2>&1
log "FIM"
touch out/DONE 2>/dev/null || { mkdir -p out; touch out/DONE; }
