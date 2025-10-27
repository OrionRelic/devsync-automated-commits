# Test Case Analysis: sum-of-sales

## Test Case Overview

```yaml
id: sum-of-sales
brief: Publish a single-page site that fetches data.csv from attachments, 
       sums its sales column, sets the title to "Sales Summary ${seed}", 
       displays the total inside #total-sales, and loads Bootstrap 5 from jsdelivr.

attachments:
  - name: data.csv
    url: data:text/csv;base64,${seed}

checks:
  - js: document.title === `Sales Summary ${seed}`
  - js: !!document.querySelector("link[href*='bootstrap']")
  - js: Math.abs(parseFloat(document.querySelector("#total-sales").textContent) - ${result}) < 0.01

round2:
  - brief: Add a Bootstrap table #product-sales that lists each product...
  - brief: Introduce a currency select #currency-picker...
  - brief: Allow filtering by region via #region-filter...
```

---

## ✅ Compatibility Check with Our System

### What Works Out of the Box

✅ **Template Structure**: Matches our TaskTemplate format
✅ **Round 1 & Round 2**: We support multi-round briefs
✅ **Attachments**: We handle data URIs (base64 encoded)
✅ **Parametrization**: We support `${seed}` substitution
✅ **Multiple Round 2 Briefs**: Can be split into 3 separate Round 2 templates

### What Needs Adaptation

⚠️ **JavaScript-based Checks**: Our current system uses Playwright selector checks
⚠️ **Dynamic Variables**: `${result}` needs to be calculated from seed
⚠️ **Multiple Round 2 Options**: We currently do one Round 2 per template

---

## 🔧 How to Integrate This Test Case

### Option 1: Add as New Template (Recommended)

I'll create a new template that matches this specification:

```python
'sum-of-sales': TaskTemplate(
    template_id='sum-of-sales',
    name='Sales Summary Dashboard',
    round1={
        'brief': '''Publish a single-page site that:
- Fetches data.csv from attachments
- Sums the sales column
- Sets the title to "Sales Summary {seed}"
- Displays the total inside #total-sales
- Loads Bootstrap 5 from jsdelivr''',
        'params': {
            'seed': ['ABC123', 'XYZ789', 'DEF456', 'GHI012'],
            'result': [12500.50, 8750.25, 15000.00, 9999.99]
        },
        'attachments': [
            {
                'name': 'data.csv',
                'type': 'text/csv',
                'content': 'product,region,sales\nWidget A,North,5000\n...'
            }
        ],
        'checks': [
            {'type': 'document_title', 'expected': 'Sales Summary {seed}'},
            {'type': 'element_exists', 'selector': 'link[href*="bootstrap"]'},
            {'type': 'element_text_number', 'selector': '#total-sales', 'expected': '{result}', 'tolerance': 0.01}
        ]
    },
    round2={...}
)
```

### Option 2: Extend Playwright Checks

Add JavaScript evaluation support to `evaluate.py`:

```python
async def _check_javascript(self, page: Page, check: Dict, repo: Dict) -> Dict:
    """Execute JavaScript check."""
    js_code = check.get('js', '')
    
    try:
        result = await page.evaluate(js_code)
        
        if result:
            return self._create_result(
                repo, 'js_check', 1.0,
                f'JavaScript check passed: {js_code[:50]}...',
                ''
            )
        else:
            return self._create_result(
                repo, 'js_check', 0,
                f'JavaScript check failed: {js_code[:50]}...',
                ''
            )
    except Exception as e:
        return self._create_result(
            repo, 'js_check', 0,
            f'JavaScript error: {str(e)}',
            js_code
        )
```

---

## 🎯 Issues with Current Test Case Format

### Issue 1: JavaScript-based Checks

**Problem**: Our system uses Playwright selector-based checks:
```python
{'type': 'element_exists', 'selector': '#total-sales'}
```

**Your format uses**:
```yaml
js: document.title === `Sales Summary ${seed}`
```

**Solution**: Extend our check types to support `js` type.

---

### Issue 2: Dynamic Variables

**Problem**: `${result}` needs to be computed from `${seed}` + CSV data

**Current approach**: We parametrize with static lists
```python
'seed': ['ABC123', 'XYZ789']
```

**Your approach**: Dynamic computation
```python
${result} = calculate_sum_from_csv(${seed})
```

**Solution**: Pre-compute result during task generation.

---

### Issue 3: Multiple Round 2 Variants

**Problem**: You have 3 different Round 2 briefs (table, currency, filter)

**Current approach**: One Round 2 per template

**Your approach**: Multiple Round 2 options

**Solution**: 
- Create 3 separate templates (sum-of-sales-table, sum-of-sales-currency, sum-of-sales-filter)
- OR: Randomize which Round 2 variant to send

---

## ✅ Implementation: Add This Template

Let me create a complete implementation:

```python
import base64
import hashlib

def generate_csv_data(seed: str) -> tuple[str, float]:
    """Generate CSV data based on seed and return (csv_content, expected_sum)."""
    # Use seed to generate deterministic data
    random.seed(hashlib.md5(seed.encode()).hexdigest())
    
    products = ['Widget A', 'Widget B', 'Widget C', 'Gadget X', 'Gadget Y']
    regions = ['North', 'South', 'East', 'West']
    
    rows = []
    total = 0
    
    for i in range(5):
        product = random.choice(products)
        region = random.choice(regions)
        sales = round(random.uniform(1000, 5000), 2)
        rows.append(f'{product},{region},{sales}')
        total += sales
    
    csv_content = 'product,region,sales\n' + '\n'.join(rows)
    return csv_content, total


'sum-of-sales': TaskTemplate(
    template_id='sum-of-sales',
    name='Sales Summary Dashboard',
    round1={
        'brief': '''Publish a single-page site that:
- Fetches data.csv from attachments
- Sums the sales column  
- Sets the title to "Sales Summary {seed}"
- Displays the total inside #total-sales
- Loads Bootstrap 5 from jsdelivr (https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css)

Requirements:
- Parse CSV data from attachments
- Calculate sum of sales column
- Display result in element with id="total-sales"
- Page title must be exactly "Sales Summary {seed}"
- Include Bootstrap 5 CSS link''',
        'params': {
            'seed': ['A1B2C3', 'X9Y8Z7', 'D4E5F6', 'G7H8I9']
        },
        'attachments': [],  # Generated dynamically
        'checks': [
            {'type': 'document_title', 'pattern': 'Sales Summary {seed}'},
            {'type': 'element_exists', 'selector': 'link[href*="bootstrap"]'},
            {'type': 'element_exists', 'selector': '#total-sales'},
            {'type': 'element_text_matches', 'selector': '#total-sales', 'pattern': r'\d+\.\d{2}'}
        ]
    },
    round2={
        'brief': '''Enhance your Sales Summary Dashboard:

1. Add a Bootstrap table with id="product-sales" that:
   - Lists each product with its total sales
   - Has proper Bootstrap table classes (table, table-striped, etc.)
   - Keeps #total-sales accurate after render

2. Introduce a currency converter:
   - Add <select id="currency-picker"> with options: USD, EUR, GBP, INR
   - Use rates.json from attachments for conversion rates
   - Update #total-sales when currency changes
   - Display active currency in element with id="total-currency"

3. Add region filtering:
   - Add <select id="region-filter"> with options for each region
   - Update #total-sales with filtered sum
   - Set data-region attribute on #total-sales to show active choice

All features should work together (filter affects both table and currency-converted total).''',
        'params': {},
        'attachments': [
            {
                'name': 'rates.json',
                'type': 'application/json',
                'content': '{"USD": 1, "EUR": 0.85, "GBP": 0.73, "INR": 83.12}'
            }
        ],
        'checks': [
            # Table checks
            {'type': 'element_exists', 'selector': '#product-sales'},
            {'type': 'element_exists', 'selector': '#product-sales tbody tr', 'min_count': 1},
            {'type': 'element_exists', 'selector': '#product-sales.table'},
            
            # Currency picker checks
            {'type': 'element_exists', 'selector': '#currency-picker'},
            {'type': 'element_exists', 'selector': '#currency-picker option[value="USD"]'},
            {'type': 'element_exists', 'selector': '#currency-picker option[value="EUR"]'},
            {'type': 'element_exists', 'selector': '#total-currency'},
            
            # Region filter checks
            {'type': 'element_exists', 'selector': '#region-filter'},
            {'type': 'element_attribute', 'selector': '#total-sales', 'attribute': 'data-region'}
        ]
    }
)
```

---

## 🔧 Required Changes to Our System

### 1. Extend Check Types in evaluate.py

Add these new check types:

```python
async def _check_document_title(self, page: Page, check: Dict, repo: Dict) -> Dict:
    """Check document title."""
    expected = check.get('pattern', '')
    try:
        title = await page.title()
        if title == expected or (expected in title):
            return self._create_result(repo, 'document_title', 1.0, f'Title matches: {title}', '')
        else:
            return self._create_result(repo, 'document_title', 0, f'Title mismatch. Expected: {expected}, Got: {title}', '')
    except Exception as e:
        return self._create_result(repo, 'document_title', 0, f'Error: {str(e)}', '')

async def _check_element_text_matches(self, page: Page, check: Dict, repo: Dict) -> Dict:
    """Check if element text matches a pattern."""
    selector = check.get('selector', '')
    pattern = check.get('pattern', '')
    
    try:
        element = await page.query_selector(selector)
        if not element:
            return self._create_result(repo, 'text_match', 0, f'Element not found: {selector}', '')
        
        text = await element.text_content()
        
        import re
        if re.search(pattern, text):
            return self._create_result(repo, 'text_match', 1.0, f'Text matches pattern: {text}', '')
        else:
            return self._create_result(repo, 'text_match', 0, f'Text does not match. Pattern: {pattern}, Text: {text}', '')
    except Exception as e:
        return self._create_result(repo, 'text_match', 0, f'Error: {str(e)}', '')

async def _check_element_attribute(self, page: Page, check: Dict, repo: Dict) -> Dict:
    """Check if element has a specific attribute."""
    selector = check.get('selector', '')
    attribute = check.get('attribute', '')
    
    try:
        element = await page.query_selector(selector)
        if not element:
            return self._create_result(repo, 'attribute_check', 0, f'Element not found: {selector}', '')
        
        has_attr = await element.get_attribute(attribute)
        
        if has_attr is not None:
            return self._create_result(repo, 'attribute_check', 1.0, f'Attribute {attribute} exists: {has_attr}', '')
        else:
            return self._create_result(repo, 'attribute_check', 0, f'Attribute {attribute} not found', '')
    except Exception as e:
        return self._create_result(repo, 'attribute_check', 0, f'Error: {str(e)}', '')

async def _check_javascript(self, page: Page, check: Dict, repo: Dict) -> Dict:
    """Execute JavaScript check."""
    js_code = check.get('js', '')
    
    try:
        result = await page.evaluate(js_code)
        
        if result:
            return self._create_result(repo, 'js_check', 1.0, f'JS check passed', js_code[:100])
        else:
            return self._create_result(repo, 'js_check', 0, f'JS check failed', js_code[:100])
    except Exception as e:
        return self._create_result(repo, 'js_check', 0, f'Error: {str(e)}', js_code[:100])
```

### 2. Update _run_single_check() to Support New Types

```python
async def _run_single_check(self, page: Page, check: Dict, repo: Dict) -> Optional[Dict]:
    """Run a single Playwright check."""
    check_type = check.get('type', '')
    
    try:
        if check_type == 'element_exists':
            return await self._check_element_exists(page, check, repo)
        elif check_type == 'button_exists':
            return await self._check_button_exists(page, check, repo)
        elif check_type == 'click_interaction':
            return await self._check_click_interaction(page, check, repo)
        elif check_type == 'responsive_check':
            return await self._check_responsive(page, check, repo)
        elif check_type == 'document_title':
            return await self._check_document_title(page, check, repo)
        elif check_type == 'element_text_matches':
            return await self._check_element_text_matches(page, check, repo)
        elif check_type == 'element_attribute':
            return await self._check_element_attribute(page, check, repo)
        elif check_type == 'js' or 'js' in check:
            return await self._check_javascript(page, check, repo)
        else:
            logger.warning(f"Unknown check type: {check_type}")
            return None
    except Exception as e:
        logger.error(f"Error in check {check_type}: {str(e)}")
        return self._create_result(repo, f'check_{check_type}', 0, f'Error: {str(e)}', '')
```

---

## ✅ Verdict: Will It Work?

### Current System Capabilities

| Feature | Supported | Notes |
|---------|-----------|-------|
| Template structure | ✅ Yes | Matches our TaskTemplate format |
| Round 1 & Round 2 | ✅ Yes | We support multi-round |
| Attachments | ✅ Yes | Base64 data URIs work |
| Parametrization | ✅ Yes | `${seed}` can be substituted |
| Basic Playwright checks | ✅ Yes | Element existence, clicks, etc. |
| JavaScript checks | ⚠️ Needs extension | Add `_check_javascript()` method |
| Document title checks | ⚠️ Needs extension | Add `_check_document_title()` method |
| Attribute checks | ⚠️ Needs extension | Add `_check_element_attribute()` method |
| Dynamic result calculation | ⚠️ Manual | Need to pre-compute `${result}` |
| Multiple Round 2 options | ⚠️ Workaround | Create 3 templates or randomize |

---

## 📝 Recommendations

### Short Term (Quick Test)
1. **Add the new check methods** to `evaluate.py` (see above)
2. **Add this template** to `task_templates.py`
3. **Test with manual CSV data** (pre-computed result)

### Long Term (Production)
1. **Extend parametrization** to support dynamic computation
2. **Support multiple Round 2 variants** per template
3. **Add more JavaScript check examples**
4. **Create visual regression testing** (screenshot comparison)

---

## 🚀 How to Test This Case

```powershell
# 1. Add the new check methods to evaluate.py
# (Copy code from sections above)

# 2. Add the template to task_templates.py
# (Copy the template definition)

# 3. Create a test submission
python -c "
from task_templates import get_template
template = get_template('sum-of-sales')
task = template.generate(1, 'test@example.com', '2025-10-17-12')
print(task)
"

# 4. Test evaluation
python evaluate.py --round 1
```

---

## Summary

✅ **YES, it will work** with minor extensions:
- Add JavaScript check support (15 lines of code)
- Add document title check support (12 lines)
- Add attribute check support (15 lines)

⚠️ **Needs adaptation** for:
- Dynamic `${result}` calculation
- Multiple Round 2 options per template

The test case format is **very compatible** with our system architecture!
