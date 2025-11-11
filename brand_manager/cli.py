"""
Command-line interface for AI Brand Manager
"""
import json
import os
import sys
import click
from pathlib import Path
from dotenv import load_dotenv
from colorama import init, Fore, Style

from .models import BrandIdentity, ContentRequest
from .ai_manager import AIBrandManager

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Load environment variables
load_dotenv()

CONFIG_FILE = "brand_config.json"


def load_brand_config() -> BrandIdentity:
    """Load brand configuration from file"""
    if not os.path.exists(CONFIG_FILE):
        return None
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return BrandIdentity(**data)
    except Exception as e:
        click.echo(f"{Fore.RED}Error loading brand config: {e}")
        return None


def save_brand_config(brand: BrandIdentity):
    """Save brand configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(brand.model_dump(), f, indent=2)
        click.echo(f"{Fore.GREEN}✓ Brand configuration saved to {CONFIG_FILE}")
    except Exception as e:
        click.echo(f"{Fore.RED}Error saving brand config: {e}")


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """AI Brand Manager - Your intelligent personal brand assistant"""
    pass


@cli.command()
@click.option('--name', prompt='Brand name', help='Your brand name')
@click.option('--tagline', help='Brand tagline (optional)')
@click.option('--description', help='Brand description (optional)')
@click.option('--industry', help='Industry or sector (optional)')
@click.option('--voice', help='Brand voice/tone (e.g., professional, casual) (optional)')
@click.option('--target-audience', help='Target audience description (optional)')
def setup(name, tagline, description, industry, voice, target_audience):
    """Set up your brand identity"""
    click.echo(f"\n{Fore.CYAN}Setting up your brand identity...")
    
    # Collect values
    values = []
    click.echo(f"\n{Fore.YELLOW}Enter core brand values (press Enter with empty value to finish):")
    while True:
        value = click.prompt('Value', default='', show_default=False)
        if not value:
            break
        values.append(value)
    
    # Collect USPs
    usps = []
    click.echo(f"\n{Fore.YELLOW}Enter unique selling points (press Enter with empty value to finish):")
    while True:
        usp = click.prompt('USP', default='', show_default=False)
        if not usp:
            break
        usps.append(usp)
    
    brand = BrandIdentity(
        name=name,
        tagline=tagline,
        description=description,
        values=values,
        target_audience=target_audience,
        voice=voice,
        industry=industry,
        unique_selling_points=usps
    )
    
    save_brand_config(brand)
    
    click.echo(f"\n{Fore.GREEN}✓ Brand identity created successfully!")
    click.echo(f"\n{Fore.CYAN}Your Brand Summary:")
    click.echo(f"{Fore.WHITE}Name: {brand.name}")
    if brand.tagline:
        click.echo(f"Tagline: {brand.tagline}")
    if brand.values:
        click.echo(f"Values: {', '.join(brand.values)}")


@cli.command()
def show():
    """Show current brand identity"""
    brand = load_brand_config()
    
    if not brand:
        click.echo(f"{Fore.YELLOW}No brand configured. Run 'brand-manager setup' first.")
        return
    
    click.echo(f"\n{Fore.CYAN}=== Your Brand Identity ==={Style.RESET_ALL}")
    click.echo(f"\n{Fore.GREEN}Name:{Style.RESET_ALL} {brand.name}")
    
    if brand.tagline:
        click.echo(f"{Fore.GREEN}Tagline:{Style.RESET_ALL} {brand.tagline}")
    
    if brand.description:
        click.echo(f"{Fore.GREEN}Description:{Style.RESET_ALL} {brand.description}")
    
    if brand.industry:
        click.echo(f"{Fore.GREEN}Industry:{Style.RESET_ALL} {brand.industry}")
    
    if brand.voice:
        click.echo(f"{Fore.GREEN}Voice:{Style.RESET_ALL} {brand.voice}")
    
    if brand.target_audience:
        click.echo(f"{Fore.GREEN}Target Audience:{Style.RESET_ALL} {brand.target_audience}")
    
    if brand.values:
        click.echo(f"{Fore.GREEN}Core Values:{Style.RESET_ALL} {', '.join(brand.values)}")
    
    if brand.unique_selling_points:
        click.echo(f"{Fore.GREEN}Unique Selling Points:{Style.RESET_ALL}")
        for usp in brand.unique_selling_points:
            click.echo(f"  • {usp}")
    
    click.echo()


@cli.command()
@click.option('--count', default=3, help='Number of tagline variations to generate')
def generate_tagline(count):
    """Generate tagline suggestions using AI"""
    brand = load_brand_config()
    
    if not brand:
        click.echo(f"{Fore.YELLOW}No brand configured. Run 'brand-manager setup' first.")
        return
    
    try:
        manager = AIBrandManager()
        manager.set_brand_identity(brand)
        
        click.echo(f"\n{Fore.CYAN}Generating {count} tagline suggestions...")
        taglines = manager.generate_tagline(variations=count)
        
        click.echo(f"\n{Fore.GREEN}=== Tagline Suggestions ==={Style.RESET_ALL}\n")
        for i, tagline in enumerate(taglines, 1):
            click.echo(f"{Fore.YELLOW}{i}.{Style.RESET_ALL} {tagline}")
        click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")
        click.echo(f"{Fore.YELLOW}Make sure you have set OPENAI_API_KEY in your .env file")


@cli.command()
@click.option('--type', 'content_type', 
              type=click.Choice(['social_post', 'blog_title', 'slogan', 'product_description', 'email_subject', 'ad_copy']),
              default='social_post', help='Type of content to generate')
@click.option('--topic', help='Topic or theme for the content')
@click.option('--platform', help='Platform (e.g., twitter, linkedin, instagram)')
@click.option('--length', type=click.Choice(['short', 'medium', 'long']), default='medium', help='Desired length')
@click.option('--tone', help='Tone override (optional)')
def generate(content_type, topic, platform, length, tone):
    """Generate brand content using AI"""
    brand = load_brand_config()
    
    if not brand:
        click.echo(f"{Fore.YELLOW}No brand configured. Run 'brand-manager setup' first.")
        return
    
    try:
        manager = AIBrandManager()
        manager.set_brand_identity(brand)
        
        request = ContentRequest(
            content_type=content_type,
            topic=topic,
            platform=platform,
            length=length,
            tone=tone
        )
        
        click.echo(f"\n{Fore.CYAN}Generating {content_type}...")
        content = manager.generate_content(request)
        
        click.echo(f"\n{Fore.GREEN}=== Generated Content ==={Style.RESET_ALL}\n")
        click.echo(f"{content}\n")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")
        click.echo(f"{Fore.YELLOW}Make sure you have set OPENAI_API_KEY in your .env file")


@cli.command()
@click.argument('message')
def analyze(message):
    """Analyze if a message aligns with your brand"""
    brand = load_brand_config()
    
    if not brand:
        click.echo(f"{Fore.YELLOW}No brand configured. Run 'brand-manager setup' first.")
        return
    
    try:
        manager = AIBrandManager()
        manager.set_brand_identity(brand)
        
        click.echo(f"\n{Fore.CYAN}Analyzing message for brand alignment...")
        result = manager.analyze_brand_message(message)
        
        click.echo(f"\n{Fore.GREEN}=== Brand Alignment Analysis ==={Style.RESET_ALL}\n")
        click.echo(f"{Fore.YELLOW}Message:{Style.RESET_ALL} {result['message']}\n")
        click.echo(result['analysis'])
        click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")
        click.echo(f"{Fore.YELLOW}Make sure you have set OPENAI_API_KEY in your .env file")


@cli.command()
@click.argument('question')
def advice(question):
    """Get strategic brand advice from AI"""
    brand = load_brand_config()
    
    if not brand:
        click.echo(f"{Fore.YELLOW}No brand configured. Run 'brand-manager setup' first.")
        return
    
    try:
        manager = AIBrandManager()
        manager.set_brand_identity(brand)
        
        click.echo(f"\n{Fore.CYAN}Getting strategic advice...")
        advice_text = manager.get_brand_strategy_advice(question)
        
        click.echo(f"\n{Fore.GREEN}=== Strategic Advice ==={Style.RESET_ALL}\n")
        click.echo(f"{Fore.YELLOW}Question:{Style.RESET_ALL} {question}\n")
        click.echo(advice_text)
        click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")
        click.echo(f"{Fore.YELLOW}Make sure you have set OPENAI_API_KEY in your .env file")


@cli.command()
@click.argument('goal')
@click.option('--count', default=5, help='Number of campaign ideas to generate')
def campaign(goal, count):
    """Brainstorm campaign ideas for a specific goal"""
    brand = load_brand_config()
    
    if not brand:
        click.echo(f"{Fore.YELLOW}No brand configured. Run 'brand-manager setup' first.")
        return
    
    try:
        manager = AIBrandManager()
        manager.set_brand_identity(brand)
        
        click.echo(f"\n{Fore.CYAN}Brainstorming {count} campaign ideas...")
        ideas = manager.brainstorm_campaign_ideas(goal, num_ideas=count)
        
        click.echo(f"\n{Fore.GREEN}=== Campaign Ideas ==={Style.RESET_ALL}\n")
        click.echo(f"{Fore.YELLOW}Goal:{Style.RESET_ALL} {goal}\n")
        
        for i, idea in enumerate(ideas, 1):
            click.echo(f"{Fore.CYAN}Idea {i}:{Style.RESET_ALL}")
            click.echo(idea)
            click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}")
        click.echo(f"{Fore.YELLOW}Make sure you have set OPENAI_API_KEY in your .env file")


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == '__main__':
    main()
