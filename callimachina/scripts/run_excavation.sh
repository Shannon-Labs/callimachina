#!/bin/bash

# CALLIMACHINA v3.0 Daily Excavation Script
# Usage: ./run_excavation.sh [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
CONFIG_FILE="config/daily.yml"
OUTPUT_DIR="discoveries"
LOG_FILE="logs/excavation_$(date +%Y%m%d_%H%M%S).log"
VERBOSE=false
TEST_MODE=false

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}==== $1 ====${NC}"
}

# Function to display usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

CALLIMACHINA v3.0 Daily Excavation Script

OPTIONS:
    -c, --config FILE       Configuration file (default: config/daily.yml)
    -o, --output DIR        Output directory (default: discoveries)
    -l, --log FILE          Log file path
    -t, --test              Test mode (no actual scraping)
    -v, --verbose           Verbose output
    -h, --help              Show this help message
    -w, --work WORK_ID      Process specific work only
    -p, --priority N        Process top N priority works
    -n, --notify EMAIL      Email for notifications

EXAMPLES:
    # Run daily excavation with default settings
    $0

    # Run with custom config
    $0 -c config/custom.yml

    # Test mode (no scraping)
    $0 -t

    # Process specific work
    $0 -w "Eratosthenes.Geographika.Book3"

    # Process top 5 priority works
    $0 -p 5

EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--config)
            CONFIG_FILE="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -l|--log)
            LOG_FILE="$2"
            shift 2
            ;;
        -t|--test)
            TEST_MODE=true
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -w|--work)
            SPECIFIC_WORK="$2"
            shift 2
            ;;
        -p|--priority)
            PRIORITY_COUNT="$2"
            shift 2
            ;;
        -n|--notify)
            NOTIFY_EMAIL="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Create necessary directories
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$OUTPUT_DIR"
mkdir -p "data/fragments"
mkdir -p "data/networks"

# Function to log messages
log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
    if [ "$VERBOSE" = true ]; then
        echo "[$level] $message"
    fi
}

# Function to run Python scripts
run_python() {
    local script="$1"
    local args="${@:2}"
    
    if [ "$VERBOSE" = true ]; then
        python "$script" $args 2>&1 | tee -a "$LOG_FILE"
    else
        python "$script" $args >> "$LOG_FILE" 2>&1
    fi
    
    return ${PIPESTATUS[0]}
}

# Main execution
main() {
    print_header "CALLIMACHINA v3.0 Daily Excavation"
    print_status "Starting excavation at $(date)"
    print_status "Configuration: $CONFIG_FILE"
    print_status "Output directory: $OUTPUT_DIR"
    print_status "Log file: $LOG_FILE"
    
    if [ "$TEST_MODE" = true ]; then
        print_warning "Running in TEST MODE - no actual scraping"
    fi
    
    log_message "INFO" "Starting daily excavation"
    log_message "INFO" "Configuration: $CONFIG_FILE"
    log_message "INFO" "Test mode: $TEST_MODE"
    
    # Step 1: Fragment scraping
    print_header "Step 1: Fragment Scraping"
    log_message "INFO" "Starting fragment scraping"
    
    if [ -n "$SPECIFIC_WORK" ]; then
        print_status "Processing specific work: $SPECIFIC_WORK"
        run_python "src/fragment_scraper.py" \
            --mode=specific \
            --work="$SPECIFIC_WORK" \
            --output="data/fragments/"
    else
        print_status "Scraping all sources"
        run_python "src/fragment_scraper.py" \
            --mode=daily \
            --output="data/fragments/" \
            --test="$TEST_MODE"
    fi
    
    if [ $? -ne 0 ]; then
        print_error "Fragment scraping failed"
        log_message "ERROR" "Fragment scraping failed"
        exit 1
    fi
    
    print_status "Fragment scraping completed"
    log_message "INFO" "Fragment scraping completed"
    
    # Step 2: Citation network analysis
    print_header "Step 2: Citation Network Analysis"
    log_message "INFO" "Starting citation network analysis"
    
    run_python "src/citation_network.py" \
        --mode=excavation \
        --fragments="data/fragments/" \
        --network-output="data/networks/citation_network.json" \
        --priority-output="discoveries/priority_queue.csv" \
        --visualize="data/networks/network.png"
    
    if [ $? -ne 0 ]; then
        print_error "Network analysis failed"
        log_message "ERROR" "Network analysis failed"
        exit 1
    fi
    
    print_status "Network analysis completed"
    log_message "INFO" "Network analysis completed"
    
    # Step 3: Bayesian reconstructions
    print_header "Step 3: Bayesian Reconstructions"
    log_message "INFO" "Starting Bayesian reconstructions"
    
    if [ -n "$SPECIFIC_WORK" ]; then
        print_status "Reconstructing specific work: $SPECIFIC_WORK"
        run_python "src/bayesian_reconstructor.py" \
            --target="$SPECIFIC_WORK" \
            --output="$OUTPUT_DIR"
    elif [ -n "$PRIORITY_COUNT" ]; then
        print_status "Processing top $PRIORITY_COUNT priority works"
        run_python "src/bayesian_reconstructor.py" \
            --mode=priority \
            --count="$PRIORITY_COUNT" \
            --output="$OUTPUT_DIR"
    else
        print_status "Reconstructing high-priority works"
        run_python "src/bayesian_reconstructor.py" \
            --mode=high-priority \
            --output="$OUTPUT_DIR"
    fi
    
    if [ $? -ne 0 ]; then
        print_error "Bayesian reconstruction failed"
        log_message "ERROR" "Bayesian reconstruction failed"
        exit 1
    fi
    
    print_status "Bayesian reconstructions completed"
    log_message "INFO" "Bayesian reconstructions completed"
    
    # Step 4: Cross-lingual mapping
    print_header "Step 4: Cross-Lingual Mapping"
    log_message "INFO" "Starting cross-lingual mapping"
    
    run_python "src/cross_lingual.py" \
        --mode=daily \
        --output="data/networks/translation_chains.json"
    
    if [ $? -ne 0 ]; then
        print_warning "Cross-lingual mapping failed (non-critical)"
        log_message "WARNING" "Cross-lingual mapping failed"
    else
        print_status "Cross-lingual mapping completed"
        log_message "INFO" "Cross-lingual mapping completed"
    fi
    
    # Step 5: Stylometric analysis
    print_header "Step 5: Stylometric Analysis"
    log_message "INFO" "Starting stylometric analysis"
    
    run_python "src/stylometric_engine.py" \
        --mode=daily \
        --output="$OUTPUT_DIR"
    
    if [ $? -ne 0 ]; then
        print_warning "Stylometric analysis failed (non-critical)"
        log_message "WARNING" "Stylometric analysis failed"
    else
        print_status "Stylometric analysis completed"
        log_message "INFO" "Stylometric analysis completed"
    fi
    
    # Step 6: Generate alerts
    print_header "Step 6: Generate Alerts"
    log_message "INFO" "Generating fragment alerts"
    
    run_python "src/fragment_alert.py" \
        --check-priority \
        --auto-notify \
        --output="logs/alerts_$(date +%Y%m%d).json"
    
    if [ $? -ne 0 ]; then
        print_warning "Alert generation failed (non-critical)"
        log_message "WARNING" "Alert generation failed"
    else
        print_status "Alerts generated"
        log_message "INFO" "Alerts generated"
    fi
    
    # Summary
    print_header "Excavation Summary"
    
    # Count new discoveries
    if [ -d "$OUTPUT_DIR" ]; then
        new_discoveries=$(find "$OUTPUT_DIR" -name "*reconstruction.json" -mtime -1 | wc -l)
        print_status "New reconstructions: $new_discoveries"
        log_message "INFO" "New reconstructions: $new_discoveries"
    fi
    
    # Count new fragments
    if [ -d "data/fragments" ]; then
        new_fragments=$(find "data/fragments" -name "*.json" -mtime -1 | wc -l)
        print_status "New fragments: $new_fragments"
        log_message "INFO" "New fragments: $new_fragments"
    fi
    
    print_status "Daily excavation completed successfully!"
    log_message "INFO" "Daily excavation completed successfully"
    
    # Send notification if email provided
    if [ -n "$NOTIFY_EMAIL" ]; then
        print_status "Sending notification to $NOTIFY_EMAIL"
        echo "CALLIMACHINA daily excavation completed. Check $LOG_FILE for details." | \
        mail -s "CALLIMACHINA Daily Excavation Complete" "$NOTIFY_EMAIL" 2>/dev/null || \
        print_warning "Failed to send email notification"
    fi
    
    return 0
}

# Error handling
trap 'print_error "Script failed on line $LINENO"; exit 1' ERR

# Run main function
main "$@"